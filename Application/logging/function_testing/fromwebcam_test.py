import sys
sys.path.insert(0, '/Users/mehargoli/Documents/College Work/18500/ScottySeat/Application')
import from_webcam
import cv2
from matplotlib import pyplot as plt

camera = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
img = from_webcam.get_frame(camera)
cv2.imwrite('test.jpg', img[0])
from_webcam.end_connection(camera)