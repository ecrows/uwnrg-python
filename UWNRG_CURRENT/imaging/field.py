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

        # TODO: Copy over show_robot implementation.

        
        raise NotImplementedError

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


    def find_rect_boundary(self, edges, type):
        """DECREPIT: Use "find_next_<linetype>_line" instead.
        
        Find the edges of a rectangular field and return line index

        Should only be called *once* at the beginning of the challenge
        Pretty hack-y way to clean up the find_eight_field method

        #TODO: Remove this function and any legacy code depending on it.

        Keyword Arguments:
        edges -- the edge-filtered input frame from the camera 
        type -- the type of edge to find

        """
        linedex = -1
        detail= 10       # look at every tenth pixel
        thresh= 6       # must have at least 5 pixels to match
        rowcount = 0
        lower_lim = 0
        upper_lim = -1

        if type == "bottom":
            for rows in edges[lower_lim:upper_lim]:
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
            for rows in edges[lower_lim:upper_lim]:
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
            for rows in edges.T[lower_lim:upper_lim]:
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
        else:
            return -1

        return linedex
