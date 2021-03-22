
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
from cv2 import cv2
import imageio
import imutils
import time
import pylab
import os

# initialize the list of tracked points, the frame counter
# and the coordinate deltas
pts = deque(maxlen=20)
counter = 0
(dx,dy) =(0,0)
directio = ""
#######################################
# read the video file
path = "A4.avi"
vid = imageio.get_reader(path,'ffmpeg')
########################################
'''
Use Opencv to cover the imageio
the main target:
    1.Number of fram
    2.the fram
'''
count = 0
print(vid.shape)
for num in range(vid):
    try:
        img = vid.get_data(num)
        img = cv2.resize(img,(256,128))
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _,im = cv2.threshold(gray_img,220,1,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        image, cnts, hier = cv2.findContours(im,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        center = None
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)

            rect = cv2.minAreaRect(c)
            box = cv2.boxPonts(rect)

            box = np.int0(box)
            cv2.drawContours(img, [box],0, (0,0,255))
        if len(cnts)>1:
            c = sorted(cnts, key= cv2.contourArea)[-2]
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(img, (int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(img, center,5,(0,0,255),-1)
            pts.append(center)
        cv2.imshow('img',img)
        fourcc = cv2.VideoWriter_fourcc('F','M','P','4')
        out = cv2.VideoWriter('output.avi',-1,20.0,(640,480))
        pylab.imsave("images/"+"image-"+str(num)+".jpg",im)
    except :
        print('Error')

os.system('ffmpeg -framerate 25 -i images/image-%00d.jpg -r 76 -s 800x600 output.avi')





