import numpy as np
import cv2
from time import sleep
capture = cv2.VideoCapture(0)
import argparse

sigma=20 # intesity of blur
swap = False
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
window_ui = 'UI'

low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

def round_up_to_odd(f):
    return np.ceil(f / 2.) * 2 + 1


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_ui, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_ui, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_ui, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_ui, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_ui, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_ui, high_V)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_detection_name)
cv2.namedWindow(window_ui)

cv2.createTrackbar(low_H_name, window_ui , low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, window_ui , high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, window_ui , low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, window_ui , high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, window_ui , low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, window_ui , high_V, max_value, on_high_V_thresh_trackbar)



parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera devide number.', default=0, type=int)
args = parser.parse_args()

while(capture.isOpened()):

    ret, frame = capture.read()
    #extract the dimensions of the frame
    small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
    d = small.shape

    # define the symetric kernel size
    kernel_size = int(round_up_to_odd(d[1]*0.01)) # the size of the gauss
    blurredImg = cv2.GaussianBlur(small,(kernel_size,kernel_size),sigma)
    frame_HSV = cv2.cvtColor(blurredImg, cv2.COLOR_BGR2HSV)
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))


    cv2.imshow(window_capture_name, blurredImg)
    cv2.imshow(window_detection_name, frame_threshold)
    #mask = cv2.inRange(blurredImg,(0,0,120),(0,0,255))
    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break
    if k == ord('s'):
        k = 0;
        if swap == True:
            swap = False
        else:
            swap = True
    if swap==False:
        img = blurredImg
    else:
        img = mask
        
    #cv2.imshow('image',img)
    sleep(0.1)

capture.release()
cv2.destroyAllWindows()
