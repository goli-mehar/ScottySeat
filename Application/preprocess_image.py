import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

#given and image, apply some image processing techniques
def preprocess(img):

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)

    #img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    #img = cv.fastNlMeansDenoising(img,None,5,10,7,21)

    return img