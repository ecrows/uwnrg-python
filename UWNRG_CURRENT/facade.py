import movement.actuators as actuators
import log as log

ACTUATOR = "ACTUATOR"

movementController = actuators.Actuators()

DIRECTION = {"CLOCKWISE" = movementController.CLOCKWISE, "CLOCKWISE" = movementController.CCLOCKWISE, "DEFAULT_MOVEMENT_MAGNITUDE" = movementController.DEFAULT_MOVEMENT_MAGNITUDE, "DOWN" = movementController.DOWN, "LEFT" = movementController.LEFT, "RIGHT" = movementController.RIGHT, "UP" = movementController.UP}

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

    movementController.move_immediate(magnitude, direction, inverted_x_axis, inverted_y_axis)
