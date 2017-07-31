"""flask UI for snakesnap"""
import json
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/snakesnap')
def snakesnap():
    return render_template('snakesnap.html')

@app.route('/signIn', methods=['GET','POST'])
def signIn():
    if request.method == 'POST':
        username = request.form['name']
        useremail = request.form['email']
        userpassword = request.form['password']
    return render_template("signin.html")

if __name__ == '__main__':
    app.run(debug = True)
