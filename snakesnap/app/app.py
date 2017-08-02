"""flask UI for snakesnap"""
import json
from flask import Flask
from flask import render_template
import os
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/snakesnap')
def snakesnap():
    logon = None
    if os.path.exists('login.json'):
        with open('login.json', 'r') as login:
            logon = json.load(login)
    return render_template('snakesnap.html', logon=logon)

@app.route('/signIn', methods=['GET','POST'])
def signIn():
    if request.method == 'POST':
        login_keys = request.form
        username = request.form['name']
        flash('Welcome '+username+' you are logged in')
        with open('login.json', 'w') as logon:
            json.dump(login_keys, logon)
        return redirect(url_for('snakesnap'))
    return render_template('signin.html')

#TODO add logout button to delete login json

if __name__ == '__main__':
    app.secret_key = 'nick'
    app.run(debug = True)
