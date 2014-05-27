import cv2 as cv2
import numpy as np
import field as field
import os as os

class MicroAssembly(field.Field):

    __leftline = -1
    __channel_left = -1
    __channel_right = -1
    __topline = -1
    __botline = -1
    __channel_top = -1
    __channel_bot = -1
    __raw_robo_pos = (-1, -1)
    __current_robo_pos = (-1, -1)
    __current_triangle_positions = () #TODO: How many triangles are in the competition?

    __clear_cmd = 'cls'

    # Simple field representation for use in pathfinding, etc.
    __field_data = ()

    def __init__(self, frame):
        """Do initial field processing and initialize character representation of field.
        
        Keyword Arguments:
        frame -- The initial camera frame to use for locating the field.
        
        """
        self.__find_field(frame)

        self.__field_data = np.zeros((self.GRID_W,self.GRID_H), dtype=np.uint8)

        # Check if these proportions are correct.
        # TODO: Pretty sure the GRID_W and GRID_H are mixed up here and there.
        
        for i in range(self.GRID_W):
            for j in range(self.GRID_H):
                if (i == 0):
                    if (j <= self.GRID_H/2):
                        self.__field_data.itemset((i,j), 1) 
                elif (i == self.GRID_W-1):
                    if (j <= self.GRID_H/2):
                        self.__field_data.itemset((i,j), 1)
                elif (i == self.GRID_W/3 or i == (self.GRID_W/3) * 2):
                    if (j > self.GRID_H/2):
                        self.__field_data.itemset((i,j), 1)
               
                if (j == 0):
                    self.__field_data.itemset((i,j), 1) 
                elif (j == self.GRID_H/2):
                    if (i <= self.GRID_W/3 or i >= (self.GRID_W/3)*2):
                        self.__field_data.itemset((i,j), 1) 
                elif (j == self.GRID_H-1):
                    if (i >= self.GRID_W/3 and i <= (self.GRID_W/3)*2):
                        self.__field_data.itemset((i,j), 1) 

        # Set up numpy for dumping the field_data array.
        np.set_printoptions(threshold=np.nan)
        # print self.__field_data

        # Get the command we need to clear the console (for debugging purposes)
        self.__clear_cmd = 'cls' if os.name == 'nt' else 'clear'

    def __find_field(self, frame):
        """Returns array representation of rectangular field. Should be called
        *once* at the beginning of the challenge. Works only on an aligned
        vertically and horizontally field, with the channel to the right.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        
        # Performs initial filtering
        # TODO: Balance arg values, link to UI for easy user adjustment
        roi = frame[120:360, 160:550]        # avoid getting frame edges detected
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        medfilt=cv2.medianBlur(gray, 7)    # aperture width must be odd.
        tr=cv2.adaptiveThreshold(medfilt,255,0,1,11,2)
        edges = cv2.Canny(medfilt, 80, 120)

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
        # TODO: This must be changed when the threshold GUI is implemented
        leftline += 160
        channel_left += 160
        channel_right += 160
        topline += 120
        botline += 120
        channel_top += 120
        channel_bot += 120

        self.__leftline = leftline
        self.__channel_left = channel_left 
        self.__channel_right = channel_right 
        self.__topline = topline 
        self.__botline = botline 
        self.__channel_top = channel_top 
        self.__channel_bot = channel_bot 

    def process_grid(self, frame):
        """Finds the robot and triangles in a camera frame, using the boundaries saved from "find_field"
        Updates the current_pos values with the new positions of the robot and triangles.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        if self.__leftline == -1:
            print "Attempted to find robot before finding field!"
            raise

        # Performs initial filtering TODO: Could still use some tweaking
        # Note that it is not necessary to perform any edge filtering
        roi = frame[self.__topline+20:self.__botline-10, self.__leftline+20:self.__channel_left-8]        # search only the area within the walls of the field 
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        #medfilt=cv2.medianBlur(gray, 1)    # aperture width must be odd.
        #tr=cv2.threshold(medfilt,40,255,1)[1]

        # TODO: if median filtering proves unnecessary, we might be able to directly threshold the frame input
        tr=cv2.threshold(gray,40,255,1)[1]

        robo_coord = self.find_blob(tr, 4)
        adjusted_robo_coord = (robo_coord[0] + self.__leftline+20, robo_coord[1] + self.__topline+20)

        # Search the channel if we didn't find it in the main area.
        # TODO: Check what happens as it crosses the boundary.  Potentially extend channel search out to the left.
        if (robo_coord[0] == -1 and robo_coord[1] == -1):
            roi = frame[self.__channel_top+20:self.__channel_bot-10, self.__channel_left:self.__channel_right-8]        # search only the area within the walls of the field 
            gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            #medfilt=cv2.medianBlur(gray, 5)    # aperture width must be odd.
            #tr=cv2.threshold(medfilt,40,255,1)[1]
            tr=cv2.threshold(gray,40,255,1)[1]
            robo_coord = self.find_blob(tr, 4)

            if (robo_coord[0] != -1):
                # TODO: These values will be dependent on the amount of extra space we're trimming.  Tweak accordingly.
                adjusted_robo_coord = (robo_coord[0] + self.__channel_left, robo_coord[1] + self.__channel_top+20)
        
        self.__raw_robo_pos = (adjusted_robo_coord[0], adjusted_robo_coord[1])

        # Scale the result onto the grid, don't update the robot position if we couldn't find it.
        # TODO: We need a handling strategy if we lose the robot and can't find it.

        if (robo_coord[0] != -1 and robo_coord[1] != -1):
            # TODO: Ensure we never place the robot on a wall.
            self.__field_data.itemset(self.__current_robo_pos, 0)

            self.__current_robo_pos = (((adjusted_robo_coord[1] - self.__topline)*self.GRID_H / (self.__botline - self.__topline)),
                                        ((adjusted_robo_coord[0] - self.__leftline)*self.GRID_W / (self.__channel_right - self.__leftline)))

            self.__field_data.itemset(self.__current_robo_pos, 9)


    def show_robot(self, frame):
        """Draw a circle at the location of the robot

        Keyword Arguments:
        image -- image to draw boundaries on
        """
        if self.__leftline == -1:
            print "Attempted to show robot before finding field!"
            raise

        """# Performs initial filtering TODO: Could still use some tweaking
        # Note that it is not necessary to perform any edge filtering
        roi = frame[self.__topline+20:self.__botline-10, self.__leftline+20:self.__channel_left-8]        # search only the area within the walls of the field 
        gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        #medfilt=cv2.medianBlur(gray, 1)    # aperture width must be odd.
        #tr=cv2.threshold(medfilt,40,255,1)[1]

        # TODO: if median filtering proves unnecessary, we might be able to directly threshold the frame input
        tr=cv2.threshold(gray,40,255,1)[1]

        robo_coord = self.find_blob(tr, 4)
        adjusted_robo_coord = (robo_coord[0] + self.__leftline+20, robo_coord[1] + self.__topline+20)

        # Search the channel if we didn't find it in the main area.
        # TODO: Check what happens as it crosses the boundary.  Potentially extend channel search out to the left.
        if (robo_coord[0] == -1 and robo_coord[1] == -1):
            roi = frame[self.__channel_top+20:self.__channel_bot-10, self.__channel_left:self.__channel_right-8]        # search only the area within the walls of the field 
            gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            #medfilt=cv2.medianBlur(gray, 5)    # aperture width must be odd.
            #tr=cv2.threshold(medfilt,40,255,1)[1]
            tr=cv2.threshold(gray,40,255,1)[1]
            robo_coord = self.find_blob(tr, 4)

            # TODO: These will be dependent on the amount of extra space we're trimming.  Tweak accordingly.
            adjusted_robo_coord = (robo_coord[0] + self.__channel_left, robo_coord[1] + self.__channel_top+20)

        # If we still haven't found the robot, indicate it by leaving the cursor in the top left 
        if (robo_coord[0] == -1 and robo_coord[1] == -1):
            adjusted_robo_coord = (0,0) 
        """

        self.process_grid(frame)

        cv2.circle(frame, self.__raw_robo_pos, 10, (0, 0, 255))
        #cv2.line(frame, (adjusted_robo_coord[1], adjusted_robo_coord[0]), (0, 0), (0,255,255), 1) 

        # Show what the current field data looks like
        os.system(self.__clear_cmd)
        print self.__field_data

        pt1 = (self.__leftline,self.__topline)
        pt2 = (self.__channel_left,self.__topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2) 

        pt1 = (self.__leftline, self.__botline)
        pt2 = (self.__channel_left, self.__botline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (self.__leftline, self.__botline)
        pt2 = (self.__leftline, self.__topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (self.__channel_right, self.__channel_top)
        pt2 = (self.__channel_right, self.__channel_bot)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (self.__channel_left, self.__channel_top)
        pt2 = (self.__channel_right, self.__channel_top)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (self.__channel_left, self.__channel_bot)
        pt2 = (self.__channel_right, self.__channel_bot)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (self.__channel_left, self.__channel_top)
        pt2 = (self.__channel_left, self.__topline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)

        pt1 = (self.__channel_left, self.__channel_bot)
        pt2 = (self.__channel_left, self.__botline)
        cv2.line(frame, pt1, pt2, (0,0,255), 2)
       

        return frame
        
        
    def show_boundaries(self, frame):
        """Attempt to find and display boundaries of field
        and return image with lines drawn on.

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
