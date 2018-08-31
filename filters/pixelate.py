from PIL import Image
import numpy as np

backgroundColor = (0,)*3
pixelSize = 4

def process_image(cv2_image):
    image = Image.fromarray(cv2_image)
    image = image.resize((image.size[0]/pixelSize, image.size[1]/pixelSize), Image.NEAREST)
    image = image.resize((image.size[0]*pixelSize, image.size[1]*pixelSize), Image.NEAREST)
    pixel = image.load()
    i_size = image.size[0]
    j_size = image.size[1]
    for i in range(0,i_size,pixelSize):
        for j in range(0,j_size,pixelSize):
            for r in range(pixelSize):
                if j+r < j_size and i+r < i_size:
                    pixel[i+r,j] = backgroundColor
                    pixel[i,j+r] = backgroundColor
    
    return np.array(image)
