"""flask UI for snakesnap"""
import os
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import Response
import cv2
#from camera import Camera  # video streaming
from leptonclass import ThermalCamera


app = Flask(__name__)


SNAKESNAP_FILES = os.path.join('static', 'snakesnap_files/')
app.config['SNAKESNAP_FILES'] = SNAKESNAP_FILES

# make snakesnap file directory if it doesn't exist.
if not os.path.isdir(SNAKESNAP_FILES):
    os.mkdir(SNAKESNAP_FILES)

thermal_class = ThermalCamera()



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
    raw_files = os.listdir(SNAKESNAP_FILES)
    files = [file for file in raw_files if file.endswith('png')]
    if not session.get('logged_in'):
        return render_template('snakesnap.html', status=False, files = files)
    return render_template('snakesnap.html', username=session.get('username', files = files))


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

# may be helpful flask.pocoo.org/docs/0.12/patterns/streaming/
@app.route('/video_feed')
def video_feed():
    try:
        print('')
        print('posting image')
        print('')
        return Response(thermal(thermal_class).next(), mimetype='multipart/x-mixed-replace;boundary=frame')
    except Exception as e:
        print('video_feed exception {}'.format(e))
        thermal_class.stop()
#@app.route('/video_feed')
#def video_feed():
#    try:
#        return Response(gen(Camera()), mimetype='multipart/x-mixed-replace;boundary=frame')
#    except:
#        pass


# def gen(camera):
#    while True:
#        frame = camera.get_frame()
#        yield(b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def thermal(thermal_class):
    try:
        thermal_class.start_thermal_thread()
        frame = thermal_class.read()

        print('getting img')
        print(frame.shape)
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        thermal_class.stop()
        print('thermal exception {}'.format(e))




# use this https://pythonspot.com/en/login-authentication-with-flask/
# and http://flask.pocoo.org/docs/0.12/quickstart/


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, threaded=True)
