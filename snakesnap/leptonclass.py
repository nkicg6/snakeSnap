import time
from threading import Thread
import cv2
import numpy as np
import imutils
from pylepton import Lepton


class ThermalCamera:
    """
    class for controlling the Lepton module
    thermal camera.
    Author: Nick George
    contact: nicholas.m.george@ucdenver.edu
    Huge thanks to Adrian Rosebrock for his excellent
    website pyimagesearch.com
    this class is heavily inspired by
    https://www.pyimagesearch.com/2015/12/28/ \
    increasing-raspberry-pi-fps-with-python-and-opencv/
    Methods:
    """

    def __init__(self, width=400, colormap=cv2.COLORMAP_JET):
        """
        Init class. Defaults work well, but you
        are welcome to change colormap to a valid opencv
        colormap and the width to an integer width for
        the image resizing.
        """
        self.width = width  # pixels, size to resize
        self.colormap = colormap  # Opencv colormap
        self.stopped = True
        self.frame = None
        self.thermal_stream = self.stream()
        self.streamed_img = None

    def start_thermal_thread(self):
        """
        start  the thread that updates
        thermal stream
        """
        global kill_thread

        thermal_thread = Thread(target=self.stream)
        thermal_thread.start()
        self.stopped = False
        return self

    def stream(self):
        """
        Infinite loop, returns normalized and
        colored frames from the lepton module
        """
        global kill_thread
        kill_thread = False
        timer = time.time()
        while not kill_thread and timer <= timer+100:
            print('STREAMMM')
            print('{}'.format(kill_thread))
            self.frame = self._lept_snap()
            time.sleep(1)  # delay 1ms
            timer = time.time()
            if self.stopped:
                kill_thread = True
                return
            return

    def _lept_snap(self):
        """
        takes the image
        """
        print('taking image')
        with Lepton() as l:
            raw, _ = l.capture()
        cv2.normalize(raw, raw, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(raw, 8, raw)
        raw = np.uint8(raw)
        adj = cv2.applyColorMap(raw, self.colormap)
        return adj

    def read(self):
        """
        resize and return the most recent frame
        """
        print('reading')
        return imutils.resize(self.frame, width=self.width)

    def stop(self):
        """
        tell the thread to stop
        """
        print('stopping')
        self.stopped = True
        kill_thread = True
