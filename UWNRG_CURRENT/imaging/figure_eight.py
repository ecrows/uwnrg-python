import cv2 as cv2
import numpy as np
import field as field

class Figure8(field.Field):
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
        medfilt=cv2.medianBlur(gray, self.medfilt_width)    # aperture width must be odd.
        tr=cv2.adaptiveThreshold(medfilt,255,0,1,self.adaptive_blocksize,self.adaptive_c)
        edges = cv2.Canny(medfilt, self.canny_thresh1, self.canny_thresh2)
        fancyedges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

        # Creates output grid, initializes boundaries around edges (wall = 2)
        # TODO: Add boundaries efficiently (i.e. one pass)
        data = np.zeros((self.GRID_H, self.GRID_W))
        data[0:self.GRID_W, 0] = 1
        data[0:self.GRID_W, self.GRID_W-1] = 1
        data[0, 0:self.GRID_H] = 1
        data[self.GRID_H-1, 0:self.GRID_H] = 1

        # Detect outer boundaries.

        topline = self.find_rect_boundary(edges, "top")
        botline = self.find_rect_boundary(edges, "bottom")
        leftline = self.find_rect_boundary(edges, "left")
        rightline = self.find_rect_boundary(edges, "right")

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
        # Temporary image output so I know what's happening

        cv2.namedWindow("Display window", cv2.CV_WINDOW_AUTOSIZE)
        cv2.imshow("Display window", fancyedges)
        cv2.waitKey()

        return (data)

    def show_boundaries(self, frame):
        """Attempt to find and display boundaries of field
        and return image with lines drawn on.

        TODO:Encapsulate boundary finding in another function.

        Keyword Arguments:
        image -- image to draw boundaries on
        """
        # Performs initial filtering
        # TODO: Balance arg values, link to UI for easy user adjustment
        roi = frame[60:475, 20:620]        # avoid getting frame edges detected
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        medfilt=cv2.medianBlur(gray, 7)    # aperture width must be odd.
        tr=cv2.adaptiveThreshold(medfilt,255,0,1,11,2)
        edges = cv2.Canny(medfilt, 80, 120)

        # Creates output grid, initializes boundaries around edges (wall = 1)
        # TODO: Add boundaries efficiently (i.e. one pass)
        data = np.zeros((self.GRID_H, self.GRID_W))
        data[0:self.GRID_W, 0] = 1
        data[0:self.GRID_W, self.GRID_W-1] = 1
        data[0, 0:self.GRID_H] = 1
        data[self.GRID_H-1, 0:self.GRID_H] = 1

        # Detect outer boundaries.

        topline = self.find_rect_boundary(edges, "top")
        botline = self.find_rect_boundary(edges, "bottom")
        leftline = self.find_rect_boundary(edges, "left")
        rightline = self.find_rect_boundary(edges, "right")

        # Update region of interest to cut down unnecessary processing
        self.roi_top = topline + 10
        self.roi_bot = botline - 10
        self.roi_left = leftline + 10
        self.roi_right = rightline - 10
        # Below are adjusted for ROI offset
        # This should be changed when the threshold GUI is implemented
        leftline += 20
        rightline += 20
        topline += 60
        botline += 60

        pt1 = (leftline,topline)
        pt2 = (rightline,topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 3) 

        pt1 = (leftline, botline)
        pt2 = (rightline, botline)
        cv2.line(frame, pt1, pt2, (0,0,255), 3)

        pt1 = (rightline, botline)
        pt2 = (rightline, topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 3)

        pt1 = (leftline, botline)
        pt2 = (leftline, topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 3)

        return frame

    def find_robot(self, frame):
        """Finds the robot given a camera frame.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        pass
