import movement.actuators as actuators
import log as log

ACTUATOR = "ACTUATOR"
CLOCKWISE = actuators.CLOCKWISE
CCLOCKWISE = actuators.CCLOCKWISE
DEFAULT_MOVEMENT_MAGNITUDE = actuators.DEFAULT_MOVEMENT_MAGNITUDE
DOWN = actuators.DOWN
LEFT = actuators.LEFT
RIGHT = actuators.RIGHT
UP = actuators.UP

#executes a single movement
def move_immediate(magnitude, direction, inverted_x_axis, inverted_y_axis, mode):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    magnitude -- scalar quantity for movement
    direciton -- direction of movement
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis
    mode -- control system to use to execute the command

    """

    if mode == ACTUATOR:
        actuators.move_immediate(magnitude, direction, inverted_x_axis, inverted_y_axis)
    else:
        log.log_error("{0} is an unknown mode.".format(mode))
