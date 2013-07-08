import imaging.image_recognition as imaging
import cv2 as cv2  
import numpy as np

#vc = cv2.VideoCapture("MobilityRun1.wmv")
vc = cv2.VideoCapture("MicroassemblyRun1.wmv")
#vc = cv2.VideoCapture(1)
rval, frame = vc.read()

irtest = imaging.ImageRecognition("micro")
testfield = irtest.new_field()

cv2.namedWindow("preview")
testfield.find_field(frame)
processed = testfield.show_robot(frame)
while (rval): 
    cv2.imshow("preview", processed)  
    processed = testfield.show_robot(frame)
    rval, frame = vc.read()

    #Should show console output of simplified array data
    #Ideally eventually in the form of the path to be taken
    #np.set_printoptions(threshold='nan')
    #print testput

    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break
#raw_input("Press key to continue")
