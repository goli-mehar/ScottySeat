import cv2, torch,time, sys
import numpy as np
from preprocess_image import preprocess

sys.path.append("../../ScottySeat/Model_Development/yolov5")
from detect import run


def main():

    #camera = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
    # #img = camera.read()

    img = cv2.imread('../../ScottySeat/Testing Images/IMG_4575 Large.jpeg')
    img = preprocess(img)
    cv2.imwrite('../../ScottySeat/b3/scottyseats/data/data.jpg', img)

    out = run(weights='yolov5s.pt',source='../../ScottySeat/b3/scottyseats/data/data.jpg'\
        , save_txt=True, nosave=True, project='../../ScottySeat/b3/scottyseats', name='data', exist_ok=True)


