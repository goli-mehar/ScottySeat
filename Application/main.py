import cv2, torch,time,json
import numpy as np
from preprocess_image import preprocess

def main():

    #argv camera path, model path, output path,
    camera = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l')

    # while True:
        #img = camera.read()

    img = cv2.imread('insert_path_here/ScottySeat/Testing Images/IMG_4575 Large.jpeg')
    img = preprocess(img)
    out = model(img)

    results = out.pandas().xyxy[0].values

    results_chairs = [res for res in results if res[-1] == 'chair']
    results_people = [res for res in results if res[-1] == 'person']
    results_table = [res for res in results if res[-1] == 'dining table']
   
    #np.savetxt(results_chairs)
    width, height = img.shape
    results = results_chairs + results_people + results_table

    with open('insert_path_here/ScottySeat/b3/scottyseats/data/data.txt', 'w') as f:
        for a in results:
            f.write(str(a[-2]))
            f.write(str(' '))
            f.write(str(float(a[0])/height))
            f.write(str(' '))
            f.write(str(float(a[1])/width))
            f.write(str(' '))
            f.write(str(float(a[2])/height))
            f.write(str(' '))
            f.write(str(float(a[3])/width))
            f.write(str('\n'))

            print(a)
        
#         time.sleep(60)

main()

