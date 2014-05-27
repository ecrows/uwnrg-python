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

    # Store location of boundary walls in frame, measured in pixels
    __leftline = -1
    __channel_left = -1
    __channel_right = -1
    __topline = -1
    __botline = -1
    __channel_top = -1
    __channel_bot = -1

    # debug variable chooses either sample video or camera feed
    # should evolve into a "Video Source" option
    __debug = 1
    __render = 0

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

    def __process_frame(self, frame):
        # TODO: Update this to properly use encapsulated code.
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

    def find_next_horiz_line(self, edges, lower_lim, upper_lim, detail, thresh):
        """Find the first horizontal line between upper and lower limits and return line index

        Keyword Arguments:
        edges -- the edge-filtered input frame from the camera 
        lower_lim -- the lower coordinate limit to start searching
        upper_lim -- the upper coordinate limit to stop searching
        detail -- look at every "n" pixels
        thresh -- number of dark pixels to trigger a match

        """
        linedex = -1
        rowcount = 0

        for rows in edges.T[lower_lim:upper_lim]:
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

        return linedex

    def find_next_vert_line(self, edges, lower_lim, upper_lim, detail, thresh):
        """Find the first vertical line between upper and lower limits and return line index

        Keyword Arguments:
        edges -- the edge-filtered input frame from the camera 
        lower_lim -- the lower coordinate limit to start searching
        upper_lim -- the upper coordinate limit to stop searching
        detail -- look at every "n" pixels
        thresh -- number of dark pixels to trigger a match

        """
        linedex = -1
        rowcount = 0

        for rows in edges[lower_lim:upper_lim]:
            count = 0
            i = 0

            while i < rows.size:
                if rows[i] == 255:
                    count += 1
                i += detail

            if count > thresh:
                linedex = rowcount
                break

            rowcount+=1

        return linedex

    def find_blob(self, monoframe, detail):
        """Finds largest blob of white pixels in a monochromatic square frame,
        provided the blob is the largest object by far in the area.
        Returns a point at approximately the center, returns -1, -1 if no blob found

        Keyword Arguments:
        monoframe -- the thresholded frame from the camera
        detail -- look at every 'n' pixels
        
        """
        
        # Find the x-coordinate with the largest number of white pixels

        y_maxloc = -1
        y_max = 0
        rowcount = 0

        for rows in monoframe:
            count = 0
            i = 0

            while i < rows.size:
                if rows[i] == 255:
                    count += 1
                i += detail

            if count > y_max:
                y_max = count
                y_maxloc = rowcount

            rowcount += 1

        x_maxloc = -1
        x_max = 0
        rowcount = 0

        for rows in monoframe.T:
            count = 0
            i = 0

            while i < rows.size:
                if rows[i] == 255:
                    count += 1
                i += detail

            if count > x_max:
                x_max = count
                x_maxloc = rowcount

            rowcount += 1

        return (x_maxloc, y_maxloc)
