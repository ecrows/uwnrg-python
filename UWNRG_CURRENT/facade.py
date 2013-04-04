import numpy as np
import movement.actuators as actuators
import movement.solenoids as solenoids
import imaging.field as field
import log as log
import threading as threading

ACTUATOR = "ACTUATOR"
SOLENOID = "SOLENOID"
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
    elif mode == SOLENOID:
        solenoids.start_movement(direction, inverted_x_axis, inverted_y_axis)
    else:
        log.log_error("{0} is an unknown mode.".format(mode))

def end_movement(direction, inverted_x_axis, inverted_y_axis, mode):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    direciton -- direction of movement
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis
    mode -- control system to use to execute the command

    """

    if mode == SOLENOID:
        solenoids.end_movement(direction, inverted_x_axis, inverted_y_axis)
    elif mode != ACTUATOR:
        log.log_error("{0} is an unknown mode.".format(mode)

def init_field():
    return field.Field()

def configure_field(med_width, ad_bsize, ad_const, can_low, can_high):
    """ Update value of filters and boundaries 
    
    Keyword Arguments:
    med_width -- Median filter width
    ad_bsize -- Adaptive filter block size
    ad_const -- Adaptive filter constant offset
    can_low -- Canny filter lower threshold
    can_high -- Canny filter upper threshold
    
    """
    field.medfilt_width = med_width
    field.adaptive_blocksize = ab_bsize
    field.adaptive_c = ad_const
    field.canny_thresh1 = can_low
    field.canny_thresh2= can_high

def __work(main_field):
    """ Exists due to an oddity in python threading """
    main_field.start_camera_feed()

def start_feed(main_field):
    """ Start new thread for camera window """

    #p = Process(target=__work, args=(main_field,))
    #p.start()
    #t = threading.Thread(target=__work, args=(main_field,))
    #t.start()

def stop_feed(main_field):
    """ Signal camera thread to stop """
    main_field.stop_camera_feed()

def get_frame_np(main_field):
    """ Get a numpy array frame to display in the main window """
    return np.asarray(main_field.get_plain_frame())
