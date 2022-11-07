import cv2, torch,time, sys
import numpy as np
from preprocess_image import preprocess

class CV:

    def __init__(self, camera_path=''):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5l')
        self.camera = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

    def run(self):

        #argv camera path, model path, output path,
        
        #img = self.camera.read()

        img = cv2.imread('../../ScottySeat/Testing Images/IMG_4575 Large.jpeg')
        img = preprocess(img)
        out = self.model(img)

        results = out.pandas().xyxy[0].values

        height, width = img.shape
        results_chairs = [res for res in results if res[-1] == 'chair']
        results_people = [res for res in results if res[-1] == 'person']
        results_table = [res for res in results if res[-1] == 'dining table']
        results = results_chairs + results_people + results_table

        adj_results = []
        for obj in results:
            cl = obj[-2]
            x1, y1, x2, y2 = obj[0:4]

            x_w = np.abs(x2-x1); y_h = np.abs(y2-y1)

            x_c = np.minimum(x1, x2) + x_w/2; y_c = np.minimum(y1, y2) + y_h/2

            x_w /= width; x_c /= width
            y_c /= height; y_h /= height

            adj_results += [[cl, x_c, y_c, x_w, y_h]]


        with open('../../ScottySeat/b3/scottyseats/data/data.txt', 'w') as f:
            for a in adj_results:
                line = str(a[0]) + ' ' + str(float(a[1])) + ' ' + str(float(a[2])) \
                    + ' ' + str(float(a[3])) + ' ' + str(float(a[4])) + '\n'
                f.write(line)





