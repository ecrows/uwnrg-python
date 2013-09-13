import imaging.image_recognition as imaging
import cv2 as cv2

irtest = imaging.ImageRecognition("micro")
testfield = irtest.new_field()

cv2.namedWindow("preview")
processed = testfield.show_robot(irtest.get_frame())

while (True):
    cv2.imshow("preview", processed) 

    processed = testfield.show_robot(irtest.get_frame())

    #Should show console output of simplified array data
    #Ideally eventually in the form of the path to be taken
    #np.set_printoptions(threshold='nan')
    #print testput

    key = cv2.waitKey(1)
    if key == 27: # exit on ESC
        break

#raw_input("Press key to continue")
