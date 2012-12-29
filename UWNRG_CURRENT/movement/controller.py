import log as log
import movement.actuators as actuators

_EMMA = "EMMA"

class Controller():
    def get_available_com_ports(self):
        """ Returns a list of available com-ports """
        return actuators.get_available_com_ports()

    def __init__(self):
        """ Initializes the Controller to use the magnet schema """
        self.__control_schema = _EMMA
        self.__actuators = None

    def initialize_actuators(self, com_port):
        """ Initializes the actuators given their com-port and the number of
        actuators.

        Keyword Arguments:
        com_port -- The com-port to use to connect to the actuators.

        """
        if not self.__actuators:
            self.__actuators = actuators.Actuators(com_port)

    def move(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA:
            if len(vector) != 3:
                log.log_error("3 arguments were expected, " \
                              "{0} were given.".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.move(vector[:2],
                                      inverted_x_axis,
                                      inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Actuators need to be setup.")

    def move_to(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- position vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA:
            if len(vector) != 3:
                log.log_error("3 arguments were expected, " \
                              "{0} were given.".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.move_to(vector[:2],
                                         inverted_x_axis,
                                         inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Actuators need to be setup.")

    def switch_to_EMMA(self):
        """ Switches the controller to EMMA mode """
        log.log_info("Switched to EMMA mode")
        self.__control_schema = _EMMA

    def switch_to_copter(self):
        """ Switches the controller to copter mode """
        log.log_info("Switched to copter mode")
        self.__control_schema = _EMMA
