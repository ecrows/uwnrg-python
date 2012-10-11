from movement import actuators
import log

LEFT = actuators.LEFT
RIGHT = actuators.RIGHT
UP = actuators.UP
DOWN = actuators.DOWN
CLOCKWISE = actuators.CLOCKWISE
CCLOCKWISE = actuators.CCLOCKWISE
DEFAULT_MOVEMENT_MAGNITUDE = actuators.DEFAULT_MOVEMENT_MAGNITUDE



#executes a single movement
def moveImmediate(magnitude, direction):
    actuators.moveImmediate(magnitude, direction)
