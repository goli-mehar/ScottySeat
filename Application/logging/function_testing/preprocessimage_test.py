from preprocess_image import preprocess
import cv2
from matplotlib import pyplot as plt

#Basic Functionality Test
img = cv2.imread('/Users/mehargoli/Documents/College Work/18500/ScottySeat/Testing Images/Overhead #2.jpg')
out = preprocess(img)
plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(out)
plt.show()