import log as log
import movement.controller as controller
import time as time
import httplib as httplib
import errno
from socket import error as socket_error

class Solenoids(controller.Controller):

    DEFAULT_MOVEMENT_MAGNITUDE = 1
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    BRAKE = "BRAKE"
    conn = httplib.HTTPConnection("10.0.0.32", 80)
    solenoid_number = {LEFT : "3", RIGHT : "4", UP : "1", DOWN : "2", BRAKE : "5"}

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

        try:
            self.conn.request("OFF", self.solenoid_number[self.BRAKE])
            response = self.conn.getresponse()
            self.conn.request("ON", self.solenoid_number[direction])
            response = self.conn.getresponse()

            time.sleep(0.01)

            self.conn.request("OFF", self.solenoid_number[direction])
            response = self.conn.getresponse()
            self.conn.request("ON", self.solenoid_number[self.BRAKE])
            response = self.conn.getresponse()
        except socket_error as serr:
            print("Failed communication with HTTP server.")
