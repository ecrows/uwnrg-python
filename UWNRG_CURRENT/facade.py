import movement.controller as controller

_movement_controller = controller.Controller()

def move(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- movement vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.move(vector, inverted_x_axis, inverted_y_axis)

def move_to(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- position vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.move_to(vector, inverted_x_axis, inverted_y_axis)

def switch_to_EMMA():
    """ Switches the controller to EMMA mode """
    _movement_controller.switch_to_EMMA()

def switch_to_copter():
    """ Switches the controller to copter mode """
    _movement_controller.switch_to_copter()

def get_available_com_ports():
    """ Returns a list of available com-ports """
    return _movement_controller.get_available_com_ports()

def set_com_port(com_port):
    """ Sets the com-port to use for actuator communication """
    _movement_controller.initialize_actuators(com_port)
