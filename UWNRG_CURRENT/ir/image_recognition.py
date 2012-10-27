"""Image Recognition Module

Field-specific recognition methods are called before starting movement.
Robot-finding method should be called during runtime.
Triangle finding (when implemented) will be good.

Performance Note:
Frames must be processed within 0.033 to make 
the 30 FPS camera the bottleneck.
A small testing app I wrote puts the average filtering time per image
at 0.015 per frame.  That means the robot finding algorithm has about
0.018 seconds to run - plenty of time, especially if we preprocess
the field (which Dule says we can). 

TODO: Implement getters and setters for thresholding values etc.
TODO: Analyze code to make sure that it follows style guidelines.
TODO: Add checks to ensure code is never called out of sequence.

"""

import cv2
import time
import numpy as np
import math

class ImageRecognition:

    # Height and width of output arrray representation of field
    GRID_H = 32
    GRID_W = 32

    # Region of interest that we're limiting processing to
    # This saves time and lets us avoid any borders
    roi_top = -1
    roi_bot = -1
    roi_left = -1
    roi_right = -1

    # Type of field/challenge being performed
    # 0 = Figure Eight
    # 1 = Micro Assembly
    fieldtype = 0
    __field_data_horiz = []
    __field_data_vert = []

    def __init__(self, type):
        self.set_field_type(type)

        # TODO: Swap this with camera input for live testing.
        vc = cv2.VideoCapture("MobilityRun1.wmv")
        # vc = cv2.VideoCapture(1)

        rval, frame = vc.read()

        if (rval):
            self.generate_field(frame)
        else:
            # TODO: Replace with more apt exception
            raise NameError("Error: Could not read camera input.")


    def set_field_type(self, type):
        """Set field type value
        
        Use "EIGHT" to refer to Figure8.
        Use "MICRO" to refer to MicroAssembly.
        
        """
         
        if (type == "EIGHT"):
            fieldtype = 0
        elif (type == "MICRO"):
            fieldtype = 1
        else:
            # TODO: Make our own exception to raise here?
            raise NameError("Invalid field type specified") 

    def generate_field(self, frame):
        """Public function for finding field information"""
        if (self.fieldtype == 0):
            return self.__generate_field_eight(frame)
        elif (self.fieldtype == 1):
            return self.__generate_field_micro(frame)
        # TODO: Else, explode

    def find_robot(self, frame):
        """Public function for finding robot"""
        if (self.fieldtype == 0):
            return self._find_robot_eight(frame)
        elif (self.fieldtype == 1):
            return self._find_robot_micro(frame)
        # TODO: Else, explode

    def __find_rect_boundary(self, edges, type):
        """Find the edges of a rectangular field and return line index
       
        Pretty hack-y way to clean up the find_eight_field method
        
        TDOO: Make this less disgusting.

        """
        linedex = -1
        detail=10 # look at every tenth pixel
        thresh=8 # must have at least 8 pixels to match
        rowcount = 0

        if type == "bottom":
            for rows in edges:
                count = 0
                i = 0
                while i < rows.size:
                    if rows[i]==255:
                        count+=1
                    i+=detail
                if count > thresh:
                    linedex = rowcount
                rowcount+=1
        elif type == "top":
            for rows in edges:
                count = 0
                i = 0
                while i < rows.size:
                    if rows[i]==255:
                        count+=1
                    i+=detail
                if count > thresh:
                    linedex = rowcount
                    break
                rowcount+=1
        elif type == "right":
            for rows in edges.T:
                count = 0
                i = 0
                while i < rows.size:
                    if rows[i]==255:
                        count+=1
                    i+=detail
                if count > thresh:
                    linedex = rowcount
                rowcount+=1
        elif type == "left":
            for rows in edges.T:
                count = 0
                i = 0
                while i < rows.size:
                    if rows[i]==255:
                        count+=1
                    i+=detail
                if count > thresh:
                    linedex = rowcount
                    break
                rowcount+=1
        else:
            return -1
        return linedex

    def __show_eight_boundaries(self, image, leftline, rightline, botline, topline):
        """Draw rectangular boundaries on image specified by 'image'

        Hard-coded for rectangular field testing right now.
        
        TODO: should eventually take *lines* as input, not horiz/vert index.

        """
        pt1 = (0,topline)
        pt2 = (620,topline)
        cv2.line(image, pt1, pt2, (0,0,255), 3) 
    
        pt1 = (0, botline)
        pt2 = (620, botline)
        cv2.line(image, pt1, pt2, (0,0,255), 3)

        pt1 = (rightline, 0)
        pt2 = (rightline, 415)
        cv2.line(image, pt1, pt2, (0,0,255), 3)
    
        pt1 = (leftline, 0)
        pt2 = (leftline, 415)
        cv2.line(image, pt1, pt2, (0,0,255), 3)


    def __generate_field_eight(self, firstframe):
        """Returns array representation of rectangular field.
        

        Designed to be called once at the beginning of the challenge.
        Can be called again to ensure detection was successful.

        Currently only works on an approx aligned vert/horiz field.

        """

        # Performs initial filtering
        # TODO: Balance arg values, link to UI for easy user adjustment
        
        roi = firstframe[60:475, 20:620] # avoid getting frame edges detected
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        medfilt=cv2.medianBlur(gray, 7) # aperture width must be odd.
        tr=cv2.adaptiveThreshold(medfilt,255,0,1,11,2)
        edges = cv2.Canny(medfilt, 80, 120)
        fancyedges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

        # Creates output grid, initializes boundaries around edges
        # Walls represented by 'X'

        self.data = np.empty((self.GRID_H, self.GRID_W))
        
        i = 0
        for row in self.data:
            j = 0
            for block in row:
                if (j == 0 or j == GRID_W-1 or i == 0 or i == GRID_H-1):
                    block = 'X'
                else:
                    block = '.'
                i += 1

        # Detect outer boundaries.

        topline = self.__find_rect_boundary(edges, "top")
        botline = self.__find_rect_boundary(edges, "bottom")
        leftline = self.__find_rect_boundary(edges, "left")
        rightline = self.__find_rect_boundary(edges, "right")

        # Update region of interest to cut down unnecessary processing
        
        roi_top = topline+10 
        roi_bot = botline-10
        roi_left = leftline+10
        roi_right = rightline-10
        
        cropped_edges = edges[roi_top:roi_bot, roi_left:roi_right]

        # Should probably just set travel waypoints based on the outer field
        # boundaries and send the robot to each of them.

        # Inner walls could be added fairly trivially
        # either via detection and/or based on known field proportions

        # I honestly believe that no pathing solution will improve
        # our performance on Figure8 in terms of time.

        # We really would be better off just testing a whole bunch
        # of times with hard-coded values until we got it as fast
        # as possible.

        # We could implement such a solution in under an hour given the
        # final test setup.  It would be much faster/more reliable.
        
        # TODO:
        # I really need to know the scoring criteria.
        # Unless there's bonus points for scalability/style,
        # making detailed image recognition for Fig8 fields is a waste.

        # Save sum of feature pixels along rows and columns

        self.__field_data_horiz = np.zeros( (roi_right-roi_left) )
        self.__field_data_vert = np.zeros( (roi_bot-roi_top) )

        i = 0
        for row in cropped_edges.T:
            for pixel in row:
                if pixel == 255:
                    self.__field_data_horiz[i] += 1
            i += 1

        i = 0
        for col in cropped_edges:
            for pixel in col:
                if pixel == 255:
                    self.__field_data_vert[i] += 1
            i += 1

        # Output boundary lines for debug purposes (TODO: Remove)
        
        self.__show_eight_boundaries(fancyedges, leftline, rightline, botline, topline)

        # Temporary image output so I know what's happening (TODO: Remove)

        cv2.namedWindow("Display window", cv2.CV_WINDOW_AUTOSIZE)
        cv2.imshow("Display window", fancyedges)
        cv2.waitKey()
    
        return (self.data)

    def __find_robot_eight(self, frame):
        """Finds the robot on a figure eight field

        Saves sum of feature pixels along x and y axis
        Any substantial increase of feature pixels at a particular x-y coordinate
        is indicative of the robot being at that location.

        Robot's location is drawn on "data" as an 'E'.

        """

        roi = firstframe[roi_top:roi_bottom, roi_left:roi_right] # avoid getting frame edges detected
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        medfilt=cv2.medianBlur(gray, 7) # aperture width must be odd.
        tr=cv2.adaptiveThreshold(medfilt,255,0,1,11,2)
        cropped_edges = cv2.Canny(medfilt, 80, 120)

        __robot_field_data_horiz = np.zeros( (roi_right-roi_left) )
        __robot_field_data_vert = np.zeros( (roi_bot-roi_top) )

        i = 0
        for row in cropped_edges:
            for pixel in row:
                if pixel == 255:
                    _robot_field_data_horiz[i] += 1
            i += 1

        # TODO: Remove this second loop and condense into first iteration.
        i = 0
        for col in cropped_edges.T:
            for pixel in col:
                if pixel == 255:
                    _robot_field_data_vert[i] += 1

        # Locate robot by getting weighted average of increases in feature pixels

        robotx = -1
        roboty = -1

        i = 0
        
        denominator = 0
        numerator = 0

        for row in self.__field_data_horiz:
            if (__robot_field_data_horiz[i]-row >= 2):
                numerator += i*(__robot_field_data_horiz[i]-_row)
                denominator += (__robot_field_data_horiz[i]-_row)
            i += 1
 
        
        if denominator != 0:
            robotx = numerator/denominator
        
        i = 0
        
        denominator = 0
        numerator = 0

        for col in self.__field_data_vert:
            if (__robot_field_data_vert[i]-col >= 2):
                numerator += i*(__robot_field_data_vert[i]-col)
                denominator += (__robot_field_data_vert[i]-col)
            i += 1
 
        if denominator != 0:
            roboty = numerator/denominator                      

        # Translate absolute pixel average position to data array
        xdata = (robotx/(roi_right-roi_left))*(GRID_W-1)
        ydata = (roboty/(roi_bottom-roi_top))*(GRID_H-1) 

        # Mark approximate center of the robot
        data[xdata, ydata] = 'E'

    def __find_field_micro(self,frame):
        """Finds the boundaries of a micro-assembly field

        TODO: Implement this, along with triangle location.

        """
        pass

    def process (self):
        """Test function to see what's going on"""
        vc = cv2.VideoCapture("MobilityRun1.wmv")
        rval, frame = vc.read()

        if (rval):
            testput = self.find_field(frame)
            np.set_printoptions(threshold='nan')
            print testput

irtest = ImageRecognition("EIGHT")
irtest.process()
raw_input("Press any Key")
