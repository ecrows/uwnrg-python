import log as log
import time as time
import httplib as httplib
import errno
from socket import error as socket_error

class Solenoids():
    _DOWN = "DOWN"
    _LEFT = "LEFT"
    _RIGHT = "RIGHT"
    _UP = "UP"
    _BRAKE = "BRAKE"
    _conn = httplib.HTTPConnection("10.0.0.32", 80)
    _solenoid_number = {_LEFT : "3", _RIGHT : "4", _UP : "1", _DOWN : "2", _BRAKE : "5"}

    def move(self, vector, invert_x_axis, invert_y_axis):
        """ Given input parameters, activates the specified solenoid

        Keyword Arguments:
        direciton -- direction of movement
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        direction = ""

        if invert_x_axis:
            vector[0] *= -1

        if invert_y_axis:
            vector[1] *= -1

        if (vector[0] != 0):
            if (vector[0] > 0):
                direction = self._RIGHT
            else:
                direction = self._LEFT
        elif (vector[1] != 0):
            if (vector[1] > 0):
                direction = self._UP
            else:
                direction = self._DOWN

        try:
            self._conn.request("OFF", self._solenoid_number[self._BRAKE])
            response = self._conn.getresponse()
            self._conn.request("ON", self._solenoid_number[direction])
            response = self._conn.getresponse()

            time.sleep(0.01)

            self._conn.request("OFF", self._solenoid_number[direction])
            response = self._conn.getresponse()
            self._conn.request("ON", self._solenoid_number[self._BRAKE])
            response = self._conn.getresponse()
        except socket_error as serr:
            log.log_error("Failed communication with HTTP server.")
