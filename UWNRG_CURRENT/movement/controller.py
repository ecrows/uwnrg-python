import log as log
import movement.actuators as actuators

_EMMA_ACTUATORS = "EMMA_ACTUATORS"

class Controller():
    __actuators = None
    __solenoids = None

    def figure_eight(self, inverted_x_axis, inverted_y_axis):
        if self.__actuators:
            self.__actuators.figure_eight(inverted_x_axis,
                                          inverted_y_axis)
            #haven't implemented rotation yet
        else:
            log.log_error("Actuator have not been initialized" \
                          " with a com-port properly.")

    def get_available_com_ports(self):
        """ Returns a list of available com-ports """
        return actuators.get_available_com_ports()

    def __init__(self):
        """ Initializes the Controller to use the magnet schema """
        self.__control_schema = _EMMA_ACTUATORS

    def initialize_actuators(self, com_port):
        """ Initializes the actuators given their com-port and the number of
        actuators.

        Keyword Arguments:
        com_port -- The com-port to use to connect to the actuators.

        """
        if not self.__actuators:
            self.__actuators = actuators.Actuators(com_port)
    
    def speed_change(self, new_value, increment):
        """  Changes the speed of movement for the controller

        Keyword Arguments:
        increment -- whether the speed is increasing (1) or decreasing (-1)

        """
        if self.__control_schema == _EMMA_ACTUATORS:
            if self.__actuators:
                self.__actuators.step_change(new_value, increment)
            else:
                log.log_error("Actuator have not been initialized" \
                              " with a com-port properly.")

    def get_speed(self):
        if self.__control_schema == _EMMA_ACTUATORS:
            if self.__actuators:
                return self.__actuators.get_step()
            else:
                return actuators.get_default_speed()

    def end_move(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA_ACTUATORS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected, " \
                              "{0} were given.".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.end_move(vector[:2],
                                      inverted_x_axis,
                                      inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Actuator have not been initialized" \
                              " with a com-port properly.")

    def move(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA_ACTUATORS:
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
                log.log_error("Actuator have not been initialized" \
                              " with a com-port properly.")

    def move_to(self, vector, inverted_x_axis, inverted_y_axis):
        """ Sends the movement instruction to the appropriate control system

        Keyword Arguments:
        vector -- position vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        if self.__control_schema == _EMMA_ACTUATORS:
            if len(vector) != 3:
                log.log_error("3 arguments were expected " \
                              "({0} given).".format(len(vector)))
                return

            if self.__actuators:
                self.__actuators.move_to(vector[:2],
                                         inverted_x_axis,
                                         inverted_y_axis)
                #haven't implemented rotation yet
            else:
                log.log_error("Actuator have not been initialized" \
                              " with a com-port properly.")

    def switch_actuator_axis(self):
        """ Toggles which device is responsible for x and y axis movement """
        if self.__actuators:
            self.__actuators.switch_actuator_axis()
        else:
            log.log_error("Actuator have not been initialized" \
                          " with a com-port properly.")

    def switch_to_EMMA_actuator(self):
        """ Switches the controller to EMMA actuator mode """
        log.log_info("Switched to EMMA actuators mode")
        self.__control_schema = _EMMA_ACTUATORS
