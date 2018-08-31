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

pushedButton = NULL
cam = NULL
port = NULL


def showPrompt(text):
    print text
	result = False
    while True:
        if pushedButton == "Ok"
            result = True		    
			break
        if pushedButton == "Cancel"
            result = False		    
			break
    return result
			

def shot_callback(ch):
    print "Button"
    ret, image = cam.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	result = showPrompt("Ok?")
    if result:
        captureCam(False)
        showFilters(image, gray)
    else:
        captureCam(True)
    
def showFilters(image, gray):
    img1 = dither.process_image(image)
    img2 = halftone.process_image(image)
    img3 = pixelate.process_image(image)
    img4 = threshold.process_image(image)
	cv2.imshow("cartoon", gray)
    cv2.imshow("cartoon1", img1)
    cv2.imshow("cartoon2", img2)
    cv2.imshow("cartoon3", cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY))
    cv2.imshow("cartoon4", img4)


def setup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.IN)
    GPIO.add_event_detect(10, GPIO.FALLING, callback=shot_callback)
	# initialize the camera
    req = os.popen("ls -l /dev/video*")
    res = req.read()
    pos = res.find("/dev/video");
    index = res[pos+10:pos+12]
    port = int(index)
    captureCam(True)
	
def captureCam(bool):
    if bool:
        cam = cv2.VideoCapture(port)
    else:
        cam.release()
		cam = NULL
		

def startMain():
    setup()
    while True:
        ret, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('SnapshotTest',image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cam.release()
	
startMain()


