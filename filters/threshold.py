import cv2
import numpy as np
from PIL import Image

def process_image(cv2_image):
    grayscaled = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    return Image.fromarray(threshold)