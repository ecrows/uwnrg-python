import log as log

DEFAULT_MOVEMENT_MAGNITUDE = 1
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"

solenoid_number = {LEFT : "3", RIGHT : "4", UP : "1", DOWN : "2"}

def __init__():
    conn = httplib.HTTPConnection("10.0.0.32", 80)

def start_movement(direction, invert_x_axis, invert_y_axis):
    """ Given input parameters, activates the specified solenoid

    Keyword Arguments:
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

    conn.request("ON", solenoid_number[direction])
    response = conn.getresponse()

def end_movement(direction, invert_x_axis, invert_y_axis):
    """ Given input parameters, deactivates the specified solenoid

    Keyword Arguments:
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

    conn.request("OFF", solenoid_number[direction])
    response = conn.getresponse()
