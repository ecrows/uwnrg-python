# Output frames must be processed within 0.033 to make the camera the bottleneck.

# Current plan:
# Run the image recognition to determine the layout of the field, then just
# find the position of the robot based on changes.

import cv2
import time
import numpy as np
import math

#vc = cv2.VideoCapture(1)
vc = cv2.VideoCapture("MobilityRun1.wmv")

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

count = 0
render = 0
#render = input('Render: ')

if (render == 1):
    cv2.namedWindow("preview")

while rval:
    then = time.time()
    rval, frame = vc.read()
    if (rval==0):
        break
    # roi = frame[60:475, 20:620] # 5 frame border to avoid getting frame edges detected
    roi = frame[230:480, 40:500]
    gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    medfilt=cv2.medianBlur(gray, 7) #must be odd
    tr=cv2.adaptiveThreshold(medfilt,255,0,1,11,2)
    edges = cv2.Canny(medfilt, 80, 120)

    if (render == 1):
        cv2.imshow("preview", edges)

    key = cv2.waitKey(5)
    if key == 27: # exit on ESC
        break

    now = time.time()
    print "Time to run: ", (now-then)