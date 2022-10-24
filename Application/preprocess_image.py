import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

#given and image, apply some image processing techniques
def preprocess(img, alpha=1.3, beta=0):
    #alpha for contrast and beta for brightness

    img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    img = cv.fastNlMeansDenoisingColored(img,None,5,10,7,21)

    return img