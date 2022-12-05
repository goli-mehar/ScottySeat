#Adapted from https://github.com/jetsonhacks/USB-Camera/blob/main/face-detect-usb.py 
#Adapted from https://github.com/amirhosseinh77/JetsonYolo/blob/main/JetsonYolo.py

import cv2
import torch
import time

window_title = "YOLO_frames"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"

                       ])

def preprocess(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)

    #img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    #img = cv.fastNlMeansDenoising(img,None,5,10,7,21)

    return img

def yolo_loop():
    
    total_cap = 0
    total_img_cap = 0
    total_infer = 0
    total_preproc = 0
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            # Window
            while True:
                time_precap = time.time()
                ret_val, frame = video_capture.read()
                if ret_val:
                    print(frame.shape)
                    time_postcap = time.time()
                    proc_frame = preprocess(frame)
                    time_postproc = time.time()
                    # detection process
                    results = model(proc_frame) 
                    time_postinfer = time.time()
                    pd_results = results.pandas().xyxy[0]
                    #print(pd_results)
                    time_img_cap = time_postcap - time_precap
                    time_preproc = time_postproc - time_postcap
                    time_infer = time_postinfer - time_postproc
                    total_cap += 1
                    print(total_cap)
                    total_img_cap += time_img_cap
                    total_infer += time_infer
                    total_preproc += time_preproc
                    # plotting
                    for index,row in pd_results.iterrows():
                        # print(obj)
                        label = row['name']
                        score = row['confidence']
                        print(row['xmin'])
                        #[(xmin,ymin),(xmax,ymax)] = obj['bbox']
                        #color = Object_colors[Object_classes.index(label)]
                        frame = cv2.rectangle(frame, (int(row['xmin']),int(row['ymin'])), (int(row['xmax']),int(row['ymax'])), (255,0,0), 2) 
                        frame = cv2.putText(frame, f'{label} ({str(score)})', (int(row['xmin']),int(row['ymin'])), cv2.FONT_HERSHEY_SIMPLEX , 0.75, (255,0,0), 1, cv2.LINE_AA)

                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
                if total_cap == 100:
                    break

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
            f = open("yolo5preproc_res.txt", "a")
            f.write("Total cap:" + str(total_cap))
            f.write("Avg image cap time:" + str(total_img_cap/total_cap))
            f.write("Avg pre proc time:" + str(total_preproc/total_cap))
            print("Avg image cap time:", total_img_cap/total_cap)
            print("Avg infer time:", total_infer/total_cap)
            f.write("Avg infer time:" + str(total_infer/total_cap))
            f.close()
            
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    camera_id = "/dev/video0"
    video_capture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    yolo_loop()

