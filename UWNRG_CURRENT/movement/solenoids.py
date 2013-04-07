import log as log
import movement.controller as controller
import time as time
import httplib as httplib

class Solenoids(controller.Controller):

    DEFAULT_MOVEMENT_MAGNITUDE = 1
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    BRAKE = "BRAKE"
    conn = httplib.HTTPConnection("10.0.0.32", 80)
    solenoid_number = {LEFT : "3", RIGHT : "4", UP : "1", DOWN : "2"}

    #def __init__(self):


    def move_immediate(self, direction, invert_x_axis, invert_y_axis):
        """ Given input parameters, activates the specified solenoid

        Keyword Arguments:
        direciton -- direction of movement
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        flip = {self.LEFT : self.RIGHT, self.RIGHT : self.LEFT, self.UP : self.DOWN, 
                self.DOWN  :self.UP} 

        if (direction == self.LEFT or direction == self.RIGHT) and invert_x_axis:
            direction = flip[direction]

        if (direction == self.UP or direction == self.DOWN) and invert_y_axis:
            direction = flip[direction]

        self.conn.request("OFF", "5")
        response = self.conn.getresponse()
        self.conn.request("ON", solenoid_number[direction])
        response = self.conn.getresponse()

        time.sleep(0.01)

        self.conn.request("OFF", solenoid_number[direction])
        response = self.conn.getresponse()
        self.conn.request("ON", "5")
        response = self.conn.getresponse()
