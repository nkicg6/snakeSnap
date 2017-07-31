"""flask UI for snakesnap"""
import json
from flask import Flask
from flask import render_template
from flask import request
from flask import flash


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/snakesnap')
def snakesnap():
    return render_template('snakesnap.html')

@app.route('/signIn', methods=['GET','POST'])
def signIn():
    if request.method == 'POST':
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        flash(_name)
    if _name and _email and _password:
        return render_template('home.html')
    else:
        return render_template('signin_error.html')
if __name__ == '__main__':
    app.run(debug = True)
