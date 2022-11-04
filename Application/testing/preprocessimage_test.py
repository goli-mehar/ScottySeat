from preprocess_image import preprocess
import cv2 as cv
from matplotlib import pyplot as plt

#Basic Functionality Test
img = cv.imread('/Users/mehargoli/Documents/College Work/18500/ScottySeat/Testing Images/Overhead #2.jpg')
out = preprocess(img)
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
plt.subplot(121),plt.imshow(img, cmap='gray')
plt.subplot(122),plt.imshow(out)
plt.show()