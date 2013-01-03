import cv2 as cv2
import numpy as np
import field as field

class Figure8(field.FieldType):
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
