#Adapted from https://github.com/jetsonhacks/USB-Camera/blob/main/face-detect-usb.py 
#Adapted from https://github.com/amirhosseinh77/JetsonYolo/blob/main/JetsonYolo.py

import cv2

window_title = "YOLO_frames"

# ASSIGN CAMERA ADRESS to DEVICE HERE!
pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

def yolo_loop():

    video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            # Window
            while True:
                ret_val, frame = video_capture.read()
                if ret_val:
                    # detection process
                    objs = Object_detector.detect(frame)

                    # plotting
                    for obj in objs:
                        # print(obj)
                        label = obj['label']
                        score = obj['score']
                        [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                        color = Object_colors[Object_classes.index(label)]
                        frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2) 
                        frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)

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

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":

    yolo_loop()

