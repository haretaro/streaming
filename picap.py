import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

class PiCap:
    def __init__(self, resolution=(640,480)):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.resolution = resolution

    def read(self):
        rawCapture = PiRGBArray(self.camera, size=self.resolution)
        self.camera.capture(rawCapture, format='bgr')
        image = rawCapture.array
        ret = True if image is not None else False
        return ret, image

    def release(self):
        return

def get_capturer(use_camera_module, resolution=(640,480), device_num=0):
    if use_camera_module:
        return PiCap(resolution=resolution)
    else:
        cap = cv2.VideoCapture(device_num)
        cap.set(3, resolution[0])
        cap.set(4, resolution[1])
        return cap
