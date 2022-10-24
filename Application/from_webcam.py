#file to connect to webcam with sustained acces to sample image regularly
#code source https://www.youtube.com/watch?v=FygLqV15TxQ, https://stackoverflow.com/questions/58927474/systemerror-class-cv2-videocapture-returned-a-result-with-an-error-set
import cv2

#establish connection to camera
def establish_connection(path):
    return cv2.VideoCapture(path, cv2.CAP_AVFOUNDATION)
#signal to ensure correct connection


#function to access and sample
def get_frame(camera_object):
    return camera_object.read()


def end_connection(camera_object):
    camera_object.release()