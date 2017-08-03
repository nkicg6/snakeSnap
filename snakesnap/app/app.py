"""flask UI for snakesnap"""
import json
from flask import Flask
from flask import render_template
import os
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
app = Flask(__name__)


@app.route('/')
def home():
    """home page displayed on startup"""
    if 'name' and 'password' in session:
        return render_template('index.html', name=session['name'])
    return render_template('index.html')


@app.route('/snakesnap')
def snakesnap():
    """main user functions"""
    logon = None
    if os.path.exists('login.json'):
        with open('login.json', 'r') as login:
            logon = json.load(login)
    return render_template('snakesnap.html', logon=logon)


@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    """ Main signin page"""
    if request.method == 'POST':
        login_keys = request.form
        username = request.form['name']
        flash('Welcome '+username+' you are logged in')
        with open('login.json', 'w') as logon:
            json.dump(login_keys, logon)
        return redirect(url_for('snakesnap'))
    return render_template('signin.html')


@app.route('/logout', method=['POST'])
def logout():
    """ make logout function"""
    pass

# Fix login and logout stuff. get that figured out as session cookies.
# use this https://pythonspot.com/en/login-authentication-with-flask/
# and http://flask.pocoo.org/docs/0.12/quickstart/
# TODO reorganize into header/ footer, and name index page index.


if __name__ == '__main__':
    app.secret_key = 'nick'
    app.run(debug=True)
