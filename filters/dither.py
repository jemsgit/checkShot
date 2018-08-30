import cv2
import numpy as np
import sys
import math

def dither(img):
	"An implementation of Floyd Steinberg dithering, error diffusion dithering"
	height,width = img.shape
	out = np.zeros(img.shape,np.uint8)
	im = img.copy()
	for i in range(height-1):
		for j in range(width-1):
			old = img.item(i,j)
			new = 255 if old>127 else 0
			out.itemset(i,j,new)
			error = old-new		
			img.itemset(i,j+1,img.item(i,j+1)+error * 7/float(16))      		
      		img.itemset(i+1,j+1,img.item(i+1,j+1)+error * 3/float(16))      		
      		img.itemset(i+1,j,img.item(i+1,j)+error * 5/float(16))      		
      		img.itemset(i+1,j-1,img.item(i+1,j-1)+error * 1/float(16))
	return out

def process_image(cv2_image):
    img = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    _,th = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    dith = dither(img)
    return dith
