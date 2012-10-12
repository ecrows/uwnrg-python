import log as log

CLOCKWISE = "CLOCKWISE"
CCLOCKWISE = "CCLOCKWISE"
DEFAULT_MOVEMENT_MAGNITUDE = 1
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"

def move_immediate(magnitude, direction, invert_x_axis, invert_y_axis):
    """ Given input parameters, moves the robot appropriately

    Keyword Arguments:
    magnitude -- scalar quantity for movement
    direciton -- direction of movement
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    flip = {LEFT : RIGHT, RIGHT : LEFT, UP : DOWN, DOWN  :UP, CLOCKWISE : CCLOCKWISE, CCLOCKWISE : CLOCKWISE}

    ################################################################
    #DONT KNOW IF THIS MAKES STUFF EASIER TAYLOR, IF NOT, DELETE IT#
    if (magnitude < 0):
        direction = flip[direction]
        magnitude *= -1
    ################################################################

    if (direction == LEFT or direction == RIGHT or direction == CLOCKWISE or direction == CCLOCKWISE) and invert_x_axis:
        direction = flip[direction]

    if (direction == UP or direction == DOWN or direction == CLOCKWISE or direction == CCLOCKWISE) and invert_y_axis:
        direction = flip[direction]

    log.log_info("Move Immediate - MAGNITUDE: " + str(magnitude) + "    DIRECTION: " + str(direction))
