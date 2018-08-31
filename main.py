import cv2
import os
import RPi.GPIO as GPIO
from PIL import Image, ImageFilter
from numpy import *
from random import random
import filters.dither as dither
import filters.halftone as halftone
import filters.pixelate as pixelate
import filters.threshold as threshold

GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN)

# initialize the camera
req = os.popen("ls -l /dev/video*")
res = req.read()
pos = res.find("/dev/video");
index = res[pos+10:pos+12]
port = int(index)
cam = cv2.VideoCapture(port)

def shot_callback(ch):
    print "Button"
    ret, image = cam.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img1 = dither.process_image(image)
    img2 = halftone.process_image(image)
    img3 = pixelate.process_image(image)
    img4 = threshold.process_image(image)
	cv2.imshow("cartoon", gray)
    cv2.imshow("cartoon1", img1)
    cv2.imshow("cartoon2", img2)
    cv2.imshow("cartoon3", cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY))
    cv2.imshow("cartoon4", img4)

GPIO.add_event_detect(10, GPIO.FALLING, callback=shot_callback)

while True:
    ret, image = cam.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('SnapshotTest',image)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cam.release()
