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
processed = testfield.show_boundaries(frame)

while (rval):
    processed = testfield.show_boundaries(frame)
    cv2.imshow("preview", processed)
    #TODO: Include robot location test
    rval, frame = vc.read()
    #Should show console output of simplified array data
    #Ideally eventually in the form of the path to be taken
    #np.set_printoptions(threshold='nan')
    #print testput
    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break
#raw_input("Press any Key")
