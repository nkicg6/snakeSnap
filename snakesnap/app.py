"""flask UI for snakesnap"""
import os
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import Response
# from camera import Camera  # video streaming


app = Flask(__name__)


@app.route('/')
def home():
    """home page displayed on startup"""
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('snakesnap.html',
                               username=session.get('username'))


@app.route('/snakesnap')
def snakesnap():
    """main user functions """
    if not session.get('logged_in'):
        return render_template('snakesnap.html', status=False)
    return render_template('snakesnap.html', username=session.get('username'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """ Main signin page username control logic is
    in the html form via bootstrap css, so we don't
    need to handle errors"""
    if request.method == 'POST':
        session['logged_in'] = True
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        flash('Welcome '+session['username']+' you are logged in')
        return redirect(url_for('snakesnap'))
    return render_template('signin.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """ make logout function"""
    session['logged_in'] = False
    return home()


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/snakesnap')
def get_files(path):
    """ will return the file list if it exists"""
    raw_files = os.listdir(path)
    files = [file for file in raw_files if file.endswith('png')]
    return files


# use this https://pythonspot.com/en/login-authentication-with-flask/
# and http://flask.pocoo.org/docs/0.12/quickstart/


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, threaded=True)
