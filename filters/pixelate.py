
from PIL import Image

backgroundColor = (0,)*3
pixelSize = 4

def process_image(cv2_image):
    image = Image.fromarray(cv2_image)
    pixel = image.load()
    for i in range(0,image.size[0],pixelSize):
        for j in range(0,image.size[1],pixelSize):
            for r in range(pixelSize):
                pixel[i+r,j] = backgroundColor
                pixel[i,j+r] = backgroundColor
    
    return image
