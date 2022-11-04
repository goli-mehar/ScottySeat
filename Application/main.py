import cv2, torch,time,json
import numpy as np
from preprocess_image import preprocess

def main():

    #argv camera path, model path, output path,
    camera = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l')

    while True:
        #img = camera.read()
        img = cv2.imread('/Users/mehargoli/Documents/College Work/18500/ScottySeat/Testing Images/Overhead #2.jpg')
        img = preprocess(img)
        out = model(img)

        results = out.pandas().xyxy[0].values
        results_chairs = [res for res in results if res[-1] == 'chair']
        results_people = [res for res in results if res[-1] == 'person']
       
        #np.savetxt(results_chairs)
        
        with open('result.txt', 'w') as f:
            f.write(str(results_chairs))
        
        time.sleep(60)

main()

