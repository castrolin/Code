
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
import matplotlib.pyplot as plt

# initialize the list of tracked points, the frame counter
# and the coordinate deltas
pts = deque(maxlen=20)
counter = 0
(dx,dy) =(0,0)
directio = ""
#######################################
# read the video file
path = "A4.avi"
vid = cv2.VideoCapture(path)
NumOfFrame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
print(NumOfFrame)
########################################
##################################
# Output video repare
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('Output.avi', fourcc,5.0,(256,128))
####################################
'''
Use Opencv to cover the imageio
the main target:
    1.Number of fram
    2.the fram
'''
count = 0
for num in range(NumOfFrame):
    try:
        _,img = vid.read(num)
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _,im = cv2.threshold(gray_img,220,1,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        if sum(sum(gray_img.astype('double'))) > 1000:
            cnts, hier = cv2.findContours(im,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            center = None
            for c in cnts:
                x,y,w,h = cv2.boundingRect(c)
                #cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)

                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)

                box = np.int0(box)
                cv2.drawContours(img, [box],0, (0,0,255))
            if len(cnts)>1:
                c = sorted(cnts, key= cv2.contourArea)[-2]
                ((x,y),radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
            #deal with division by zero
                if M["m00"] != 0:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                else:
                    center = (0,0)
                CX = center[0]
                CY = center[1]
                center_string = "CX:{}, CY:{}".format(CX,CY)
                cv2.putText(img,center_string,(0,128),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                #cv2.circle(img, (int(x),int(y)),int(radius),(0,255,255),2)
                cv2.circle(img, center,5,(255,0,0),-1) # Red color
            pts.append(center)
            output_video.write(img)
    except :
        print('Error or something happend')
output_video.release()
# write the figure into video and turn
'''                
        fourcc = cv2.VideoWriter_fourcc('F','M','P','4')
        out = cv2.VideoWriter('output.avi',-1,20.0,(640,480))
        pylab.imsave("images/"+"image-"+str(num)+".jpg",im)
    except :
        print('Error', num)

os.system('ffmpeg -framerate 25 -i images/image-%00d.jpg -r 76 -s 800x600 output.avi')
'''




