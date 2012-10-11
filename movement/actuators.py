import log

LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"
DOWN = "DOWN"
CLOCKWISE = "CLOCKWISE"
CCLOCKWISE = "CCLOCKWISE"
DEFAULT_MOVEMENT_MAGNITUDE = 1

def moveImmediate(magnitude, direction):
    log.logInfo("Move Immediate - MAGNITUDE: " + str(magnitude) + "    DIRECTION: " + str(direction))
