import cv2
import numpy as np
from importlib import resources
import io

class Process:
    def __init__(self,imgPath):
        self.imgPath = imgPath
    
    def generate(self):
        image = cv2.imread(self.imgPath)
        h,w,c = image.shape
        x1 = np.random.randint(0,w//2)
        x2 = np.random.randint(x1+1,w-1)

        y1 = np.random.randint(0,h//2)
        y2 = np.random.randint(y1+1,h-1)

        imgNew = image[y1:y2, x1:x2]

        cv2.imwrite("aaa.jpg", imgNew)
        return imgNew