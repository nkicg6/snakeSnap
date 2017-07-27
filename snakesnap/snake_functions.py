""" main functions for snakeSnap"""

import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import cv2
from Lepton import Lepton
import matplotlib.pyplot as plt
import numpy as np
import picamera
from scipy import misc


def parse_json():
    """
    reads configuration info from the json
    """
    with open('snakeSnap_data.json', 'r') as jdoc:
        parsed_config = json.load(jdoc)
    return parsed_config

def update_json(parsed_config):
    """
    update json metadata
    """
    with open('snakeSnap_data.json', 'w') as jdoc:
        json.dump(parsed_config, jdoc)
        print('json updated')


def write_email(parsed_config, name, split_name):
    """
    write email info from the json dict, and attach the picture
    """
    username = parsed_config['username']
    send_to, image_name = parsed_config[split_name]
    message = parsed_config['message_path']
    # prepare the message.
    with open(message) as text:
        msgtext = text.read()
    msgtext = 'Hey '+ name + ',\n' + msgtext # add personal  name heading to the message.
    msg = MIMEMultipart()
    msg['From'] = username + '@gmail.com'
    msg['To'] = send_to
    msg['Subject'] = 'Your Snap Picture'
    with open(image_name, 'rb') as pic:
        img = MIMEImage(pic.read())
    msg.attach(MIMEText(msgtext, 'plain'))
    msg.attach(img)
    return msg

def send_email(msg, parsed_config):
    """
    Send the email and quit
    """
    username, password = parsed_config['username'], parsed_config['password']
    send_to = parsed_config[split_name]
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(username+'@gmail.com',send_to, msg.as_string())
    server.quit()
    print('Message Sent')

def thermal_pic(image_name):
    """
    do this with pylepton_overlay
    wait for input
    """
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        camera.start_preview()
        input('push enter to start')
        camera.stop_preview()
    time.sleep(1)
    # take the picture
    with Lepton() as l:
        a,_ = l.capture()
    cv2.normalize(a,a,0,65535, cv2.NORM_MINMAX)
    np.right_shift(a, 8, a)
    #note this is hacky way to read it back in and modify with matplotlib
    # future versions should fix this
    cv2.imwrite(image_name, a)
    # colormap
    cmap = plt.cm.hot
    # resize
    # again hacky I had to read it back in and re-save it.
    a = skimage.io.imread(image_name)
    bigger = misc.imresize(a, (480, 640), interp = 'bilinear')
    # save it
    plt.imsave(image_name, bigger, cmap = cmap)
    print('picture saved as ' + image_name)
