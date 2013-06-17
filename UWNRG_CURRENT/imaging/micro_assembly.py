import cv2 as cv2
import numpy as np
import field as field

class MicroAssembly(field.Field):
    def find_field(self, frame):
        """Returns array representation of rectangular field. Should be called
        *once* at the beginning of the challenge. Works only on an aligned
        vertically and horizontally field, with the channel to the right.

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
        """
        TODO: Replace with new imlpementation from show_boundaries
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

        # Temporary image output so I know what's happening

        cv2.namedWindow("Display window", cv2.CV_WINDOW_AUTOSIZE)
        cv2.imshow("Display window", fancyedges)
        cv2.waitKey()
        """
        return (data)

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

    def show_boundaries(self, frame):
        """Attempt to find and display boundaries of field
        and return image with lines drawn on.

        TODO:Encapsulate boundary finding in another function.

        Keyword Arguments:
        image -- image to draw boundaries on
        """
        # Performs initial filtering
        # TODO: Balance arg values, link to UI for easy user adjustment
        roi = frame[120:360, 160:550]        # avoid getting frame edges detected
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
        # Note that the detail and threshold values (the last two arguments) will need to be tweaked to avoid false positives

        topline = self.find_next_vert_line(edges, 0, -1, 10, 6)
        channel_top = self.find_next_vert_line(edges, topline+25, -1, 10, 6) + topline + 25
        channel_bot = self.find_next_vert_line(edges, channel_top+25, -1, 10, 6) + channel_top + 25
        botline = self.find_next_vert_line(edges, channel_bot+25, -1, 10, 6) + channel_bot + 25
        leftline = self.find_next_horiz_line(edges, 0, -1, 10, 6) 
        channel_left = self.find_next_horiz_line(edges, leftline+25, -1, 5, 6) + leftline + 25
        channel_right = self.find_next_horiz_line(edges, channel_left+25, -1, 5, 6) + channel_left+ 25

        # Below are adjusted for ROI offset
        # This should be changed when the threshold GUI is implemented
        leftline += 160
        channel_left += 160
        channel_right += 160
        topline += 120
        botline += 120
        channel_top += 120
        channel_bot += 120
        
        pt1 = (leftline,topline)
        pt2 = (channel_left,topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2) 

        pt1 = (leftline, botline)
        pt2 = (channel_left, botline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (leftline, botline)
        pt2 = (leftline, topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (channel_right, channel_top)
        pt2 = (channel_right, channel_bot)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (channel_left, channel_top)
        pt2 = (channel_right, channel_top)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (channel_left, channel_bot)
        pt2 = (channel_right, channel_bot)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (channel_left, channel_top)
        pt2 = (channel_left, topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (channel_left, channel_bot)
        pt2 = (channel_left, botline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        return frame
