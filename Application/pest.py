import cv2
from cv_class import *
print('hi')
#cv_engine = CV()

#img = cv_engine.camera.read()[1][..., ::-1] #Read in new image
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)
img = cv2.imread("/Users/mehargoli/Documents/College_Work/18500/ScottySeat/Testing_Images/IMG_4579.jpeg")
#img = cv_engine.preprocess(img) #Preprocess image
#print(img)
out = model("/Users/mehargoli/Documents/College_Work/18500/ScottySeat/Testing_Images/IMG_4579.jpeg") #Run image through model
print(out)
#bboxes = cv_engine.convert_xyxytoxywh(out, img.shape) #convert bbox dim