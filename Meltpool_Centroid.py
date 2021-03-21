
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
from cv2 import cv2
import imutils
import time
'''
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())
'''
#######################################
# read the video file
path = "A4.avi"
vid = cv2.VideoCapture(path)
########################################

#######################################
# Object algorithm
#######################################
# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
counter = 0
(dX, dY) = (0, 0)
direction = ""

# allow the camera or video file to warm up
time.sleep(2.0)

while vid.isOpened():
    ret,frame = vid.read()
    if not ret:
        break
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    _,cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if cnts != None:
        if len(cnts) > 0:
            c = max(cnts,key = cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if radius > 10:
            cv2.circle(frame, (int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(frame,center,5,(0,0,255),-1)

