import cv2 as cv2
import numpy as np
import math as math

class Field(object):
    """
    Contains methods for each field.
    
    """
    # Constant representing scale of output array
    GRID_H = 32
    GRID_W = 32

    # Region of interest that we're limiting processing to
    # This saves time and lets us avoid any borders
    # TODO: Save these settings on load.
    roi_top = 60
    roi_bot = 475
    roi_left = 20
    roi_right = 620
    medfilt_width = 7 # must be odd, should snap
    adaptive_blocksize = 11
    adaptive_c = 0
    canny_thresh1 = 80
    canny_thresh2 = 120

    # debug variable chooses either sample video or camera feed
    # should evolve into a "Video Source" option
    __debug = 1 
    __render = 0
    
    def __process_frame(self, frame):
        # 5 frame border to avoid getting frame edges detected
        roi = frame[self.roi_top:self.roi_bot, self.roi_left:self.roi_right]
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        
        if (self.medfilt_width%2 == 0):
            self.medfilt_width+=1

        medfilt=cv2.medianBlur(gray, self.medfilt_width)
        
        tr=cv2.adaptiveThreshold(medfilt,255,0,1,self.adaptive_blocksize,self.adaptive_c)

        edges = cv2.Canny(medfilt, self.canny_thresh1, self.canny_thresh2)

        return edges

    def __process_plain_frame(self, frame):
        # 5 frame border to avoid getting frame edges detected
        roi = frame[self.roi_top:self.roi_bot, self.roi_left:self.roi_right]
        return roi

    def get_plain_frame(self):
        if self.__vc.isOpened():
            rval, frame = self.__vc.read()

        if rval:
            return self.__process_plain_frame(frame)
        else:
            return False

        #TODO: Remove this debug statement
        self.__vc = cv2.VideoCapture("MobilityRun2.wmv")

    def get_frame(self):
        if self.__vc.isOpened():
            rval, frame = self.__vc.read()

        if rval:
            return self.__process_frame(frame)
        else:
            return False

    def start_camera_feed(self):
        print "Camera feed started"
        if self.__vc.isOpened(): # try to get the first frame
            rval, frame = self.__vc.read()
        else:
            rval = False

        if (self.__render == 1):
            cv2.namedWindow("Camera Feed")
            bigimage = (())

        while rval:
            rval, frame = self.__vc.read()
    
            if (rval==0):
                break

            frame = self.__process_plain_frame(frame)

            # Simple hack for large resolution viewing.
            # Should become a setting somewhere
            # Ideally just a drag to resize window
        
            bigimage = cv2.resize(frame, (840, 630))

            if (self.__render == 1):
                cv2.imshow("Camera Feed", bigimage)

            key = cv2.waitKey(5)
            if key == 27: # exit on ESC
                break

            if self.thread_running == True:
                break

        self.thread_running = False

    def stop_camera_feed(self):
        """ Stop camera feed """
        
        print "Camera feed stopped"
        self.lock.acquire()
        self.thread_running = True
        self.lock.release()

    def __show_boundaries(self, image, leftline, rightline, botline, topline):
        """ Draw rectangular boundaries on image specified by 'image'.
        Currently hardcoded for a rectangular field.

        Should be implemented by child.

        #TODO: Should eventually take *lines* as input, not horiz/vert index.

        Keyword Arguments:
        image -- image to draw boundaries on
        leftline -- leftline is the x co-ordinate of the vertical left line
        rightline -- rightline is the x co-ordinate of the vertical right line
        botline -- botline is the y co-ordinate of the horizontal left line
        topline -- topline is the y co-ordinate of the horizontal left line
        """
        raise NotImplementedError

    def __init__(self, height=32, width=32):
        """ Initializes the Field Type

        Keyword Arguments:
        height -- height of the array representing the field
        width -- width of the array representing the field

        """
        self.GRID_H = height
        self.GRID_W = width

        if self.__debug:
            self.__vc = cv2.VideoCapture("MobilityRun1.wmv")
        else:
            self.__vc = cv2.VideoCapture(1)


    def find_field(self, frame):
        """Returns array representation of rectangular field. Should be called
        *once* at the beginning of the challenge. Works only on an aligned
        vertically and horizontally field.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        raise NotImplementedError

    def find_robot(self, frame):
        """Finds the robot given a camera frame.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        """
        NOTES ON POSSIBLE IMPLEMENTATION:
        Solving this problem is likely going to be the most difficult
        part of this.

        Current plan:
        Was planning on saving the array of feature pixels on the first pass
        through, then making a pass along the y and x axis to add up the 
        feature pixels along each line.
        Any substantial increase of feature pixels at a particular x-y
        coordinate is indicative of the robot being at that location.

        The problem with this method is that the robot's initial position would
        leave a "blind spot" in the detection algorithm unless manually
        compensated for.

        Alternatively, I could save an array of feature pixels on each
        "find_robot" call. Then any increase in feature count would likely
        work.

        Further improvements to this strategy would probably be made through
        searching only areas of the field where the robot is likely to be.
        That is to say, aggressively mark around the outside boundaries and the
        middle walls and search between them for the largest clump of pixels
        (which should be the robot).

        Another question worth asking is whether the Canny filter setup
        currently used for wall detection is also the best way to detect the
        robot. There could easily exist a more conspicuous way to mark the
        robot out.
        """
        raise NotImplementedError

    def find_rect_boundary(self, edges, type):
        """Find the edges of a rectangular field and return line index

        Should only be called *once* at the beginning of the challenge
        Pretty hack-y way to clean up the find_eight_field method

        #TODO: Make this less disgusting.

        Keyword Arguments:
        edges -- the edge-filtered input frame from the camera 
        type -- the type of edge to find

        """
        linedex = -1
        detail=10       # look at every tenth pixel
        thresh=6       # must have at least 5 pixels to match
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
