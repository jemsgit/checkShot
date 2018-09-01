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
filteredImages = []
currentImageIndex = -1
printImage = NULL

def next_button_callback():
    empltyAction()

def prev_button_callback():
    empltyAction()

def cancel_button_callback():
    empltyAction()

def ok_button_callback():
    empltyAction()

def empltyAction():
    pass

def showPrompt(text):
    print text
    result = False
    while True:
        if pushedButton == "Ok":
            result = True		    
            break
        if pushedButton == "Cancel":    
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

def showNext():
    currentImageIndex+=1
    if currentImageIndex >= len(filteredImages):
        currentImageIndex = 0
    cv2.imshow("filter", filteredImages[currentImageIndex])

def showPrev():
    currentImageIndex-=1
    if currentImageIndex < 0:
        currentImageIndex = len(filteredImages) - 1
    cv2.imshow("filter", filteredImages[currentImageIndex])

def processPrint(callback):
    print "Printing image"
    callback()

def setInitialState():
    attachMenuButtons(empltyAction, empltyAction, empltyAction, empltyAction)
    captureCam(True)
    pushedButton = NULL
    filteredImages = []
    currentImageIndex = -1
    printImage = NULL

def setPrintImage(image):
    printImage = image
    processPrint(setInitialState)

def attachMenuButtons(onNext, onPrev, onCancel, onOk):
    next_button_callback = onNext
    prev_button_callback = onPrev
    cancel_button_callback = onCancel
    ok_button_callback = onOk

    
def showFilters(image, gray):
    img1 = dither.process_image(image)
    img2 = halftone.process_image(image)
    img3 = pixelate.process_image(image)
    img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    img4 = threshold.process_image(image)
    filteredImages = [gray, img1, img2, img3, img4]
    attachMenuButtons(showNext, showPrev, captureCam, )
    cv2.imshow("cartoon", gray)
    cv2.imshow("cartoon1", img1)
    cv2.imshow("cartoon2", img2)
    cv2.imshow("cartoon3", img3)
    cv2.imshow("cartoon4", img4)


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.IN)
    GPIO.add_event_detect(10, GPIO.FALLING, callback=shot_callback)
    GPIO.add_event_detect(11, GPIO.FALLING, callback=next_button_callback)
    GPIO.add_event_detect(12, GPIO.FALLING, callback=prev_button_callback)
    GPIO.add_event_detect(10, GPIO.FALLING, callback=cancel_button_callback)
    GPIO.add_event_detect(14, GPIO.FALLING, callback=ok_button_callback)
	# initialize the camera
    req = os.popen("ls -l /dev/video*")
    res = req.read()
    pos = res.find("/dev/video");
    index = res[pos+10:pos+12]
    setCameraPort(int(index))
    captureCam(True)

def setCameraPort(index):
    port = index
	
def captureCam(flag):
    if flag:
        cam = cv2.VideoCapture(port)
        ret, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('live_view',image)
    else:
        cam.release()
        cam = NULL
		

def startMain():
    setup()
    while True:
        captureCam(True)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    captureCam(False)
	
startMain()


