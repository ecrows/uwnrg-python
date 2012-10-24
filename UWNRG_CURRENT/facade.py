import movement.actuators as actuators
import log as log

ACTUATOR = "ACTUATOR"

movementController = actuators.Actuators()

#executes a single movement
def move_immediate(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- movement vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis
    mode -- control system to use to execute the command

    """

    movementController.move_immediate(vector, inverted_x_axis, inverted_y_axis)
