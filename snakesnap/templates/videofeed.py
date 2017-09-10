# adopted from http://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/
# also use http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
# and http://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/

# need to incorporate these methods to re-write the camera module and
# add the necessary callbacks to stream and take pictures.
import os
import time
import threading
import io
import picamera
from PIL import Image
import imutils
import cv2


class VideoFeed:
    def __init__(self, vs, save_spot):
        self.save_spot = save_spot
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target = self.videoLoop, args=())
        self.thread.start()

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
