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
TODO: Compensate for field angle skew?

Questions/comments/concerns/requests? Bug Evan.

"""

import cv2 as cv2
import time as time
import numpy as np
import math as math

class FieldType:
    """"""
    # Region of interest that we're limiting processing to
    # This saves time and lets us avoid any borders
    roi_top = -1
    roi_bot = -1
    roi_left = -1
    roi_right = -1

    def _show_boundaries(self, image, leftline, rightline, botline, topline):
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

    def _find_rect_boundary(self, edges, type):
        """Find the edges of a rectangular field and return line index

        Should only be called *once* at the beginning of the challenge
        Pretty hack-y way to clean up the find_eight_field method

        #TODO: Make this less disgusting.

        Keyword Arguments:
        edges -- a list of all possible edges
        type -- the type of edge to find

        """
        linedex = -1
        detail=10       # look at every tenth pixel
        thresh=8        # must have at least 8 pixels to match
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

class Figure8(FieldType):
    def find_field(self, frame):
        """Returns array representation of rectangular field. Should be called
        *once* at the beginning of the challenge. Works only on an aligned
        vertically and horizontally field.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        # Performs initial filtering
        # TODO: Balance arg values, link to UI for easy user adjustment
        roi = frame[60:475, 20:620]        # avoid getting frame edges detected
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        medfilt=cv2.medianBlur(gray, 7)    # aperture width must be odd.
        tr=cv2.adaptiveThreshold(medfilt,255,0,1,11,2)
        edges = cv2.Canny(medfilt, 80, 120)
        fancyedges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

        # Creates output grid, initializes boundaries around edges (wall = 1)
        # TODO: Add boundaries efficiently (i.e. one pass)
        data = np.zeros((self.GRID_H, self.GRID_W))
        data[0:self.GRID_W, 0] = 1
        data[0:self.GRID_W, self.GRID_W-1] = 1
        data[0, 0:self.GRID_H] = 1
        data[self.GRID_H-1, 0:self.GRID_H] = 1

        # Detect outer boundaries.

        topline = self._find_rect_boundary(edges, "top")
        botline = self._find_rect_boundary(edges, "bottom")
        leftline = self._find_rect_boundary(edges, "left")
        rightline = self._find_rect_boundary(edges, "right")

        # Update region of interest to cut down unnecessary processing
        self.roi_top = topline + 10
        self.roi_bot = botline - 10
        self.roi_left = leftline + 10
        self.roi_right = rightline - 10

        # Detect inner walls, paint them onto the output grid

        # Go from left to right.
        # Hit a white pixel?  Set the relevant grid space to '1'
        # Go along center of white pixel lines, deduce gate locations

        # Wait a second.  If we fabricate our own fields, then it would
        # be more reliable to use our own field proportions based on our outline.

        # Find top left gate (Gate 3)
        # TODO: Decrepit.  S
        """
        i = leftline+20
        centeravg = 0;
        firstval = -1
        lastval = -1
        while i < (topline+botline)/2:
            count = 0
            j = topline+10 #TODO: Balance
            while j < (leftline+rightline)/2:
                if edges[i][j]==255:
                    count+=1
                    centeravg+=j
                j+=1

            if count >= 2:
                if (firstval == -1):
                    firstval = i

                lastval = i
                centeravg/=count
                data[(i-topline)/(topline-botline)*self.GRID_H]\
                    [(centeravg-leftline)/(rightline-leftline)*self.GRID_W] = 1
            i+=1

        if (firstval != -1):
            pt1 = (centeravg, lastval)
            pt2 = (centeravg, firstval)
            cv2.line(fancyedges, pt1, pt2, (255,0,255), 3)
        #cv2.rectangle(fancyedges, centeravg, , (0,0,255), 3)
        """
        # Output boundary lines for debug purposes (TODO: Remove)
        self._show_eight_boundaries(fancyedges, leftline, rightline, botline, topline)

        # TODO: Find probable initial robot location to compensate?

        # Temporary image output so I know what's happening

        cv2.namedWindow("Display window", cv2.CV_WINDOW_AUTOSIZE)
        cv2.imshow("Display window", fancyedges)
        cv2.waitKey()

        return (data)

    def _show_boundaries(self, image, leftline, rightline, botline, topline):
        """Draw rectangular boundaries on image specified by 'image'. Currently
        hardcoded for a rectangular field.

        #TODO: Should eventually take *lines* as input, not horiz/vert index.

        Keyword Arguments:
        image -- image to draw boundaries on
        leftline -- leftline is the x co-ordinate of the vertical left line
        rightline -- rightline is the x co-ordinate of the vertical right line
        botline -- botline is the y co-ordinate of the horizontal left line
        topline -- topline is the y co-ordinate of the horizontal left line
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

    def find_robot(self, frame):
        """Finds the robot given a camera frame.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        pass

class MicroAssembly(FieldType):
    def find_field(self, frame):
        """Returns array representation of rectangular field. Should be called
        *once* at the beginning of the challenge. Works only on an aligned
        vertically and horizontally field.

        #TODO: IMPLEMENT

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        pass

    def find_robot(self):
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
        pass

class ImageRecognition:
    # Type of field/challenge being performed
    # 0 = Figure Eight
    # 1 = Micro Assembly

    def __init__(self, type="eight"):
        self.set_field_type(type)

    def set_field_type(self, type):
        """Set field type value

        Use "eight" to refer to Figure8.
        Use "micro" to refer to MicroAssembly.

        """

        if (type == "eight"):
            self.fieldtype = Figure8()
        elif (type == "micro"):
            self.fieldtype = MicroAssembly()
        else:
            # TODO: Make our own exception to raise here
            raise NameError("Invalid field type specified") 

    def find_field(self, frame):
        """Return array representation of rectangular field.
        Should be called *once* at the beginning of the challenge. Works only
        on an aligned vertically and horizontally field.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        self.fieldtype.find_field(frame)

    def find_robot(self, frame):
        """Finds the robot given a camera frame.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        self.fieldtype.find_robot(frame)

    def process (self):
        """Testing harness to see what's going on"""
        vc = cv2.VideoCapture("MobilityRun1.wmv")
        rval, frame = vc.read()

        if (rval):
            testput = self.find_field(frame)
            np.set_printoptions(threshold='nan')
            print testput

irtest = ImageRecognition()
irtest.process()
raw_input("Press any Key")
