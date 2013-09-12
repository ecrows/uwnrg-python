import log as log
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

def end_move(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the end movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- movement vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.end_move(vector, inverted_x_axis, inverted_y_axis)

def figure_eight(x_axis_inverted, y_axis_inverted):
    movements = [(0, -800, 0),
                 (800, 0, 0),
                 (0, -800, 0),
                 (-800, 0, 0),
                 (0, 800, 0),
                 (800, 0, 0),
                 (0, 800, 0),
                 (-800, 0, 0)]
    """movements = [(-800, 0, 0),
                 (0, 800, 0),
                 (-800, 0, 0),
                 (0, -800, 0),
                 (800, 0, 0),
                 (0, 800, 0),
                 (800, 0, 0),
                 (0, -800, 0)]"""
    _movement_controller.figure_eight(x_axis_inverted, y_axis_inverted)

def set_desired_current(desired_current):
    _movement_controller.set_desired_current(desired_current)

def toggle_adc():
    return _movement_controller.toggle_adc()

def get_desired_current():
    return _movement_controller.get_desired_current()

def move_to(vector, inverted_x_axis, inverted_y_axis):
    """ Sends the movement instruction to the appropriate control system

    Keyword Arguments:
    vector -- position vector
    invert_x_axis -- boolean of whether to invert on the x-axis
    invert_y_axis -- boolean of whether to invert on the y-axis

    """
    _movement_controller.move_to(vector, inverted_x_axis, inverted_y_axis)

def switch_to_EMMA_actuator():
    """ Switches the controller to EMMA actuator mode """
    _movement_controller.switch_to_EMMA_actuator()

def switch_to_EMMA_solenoid():
    """ Switches the controller to EMMA solenoid mode """
    _movement_controller.switch_to_EMMA_solenoid()

def switch_to_copter():
    """ Switches the controller to copter mode """
    _movement_controller.switch_to_copter()

def get_available_com_ports():
    """ Returns a list of available com-ports """
    return _movement_controller.get_available_com_ports()

def set_com_port(com_port):
    """ Sets the com-port to use for actuator communication """
    _movement_controller.initialize_actuators(com_port)

def switch_actuator_axis():
    """ Toggles which device is responsible for x and y axis movement """
    _movement_controller.switch_actuator_axis()

def get_speed():
    """  Changes the speed of movement for the controller

    Keyword Arguments:
    increment -- whether the speed is increasing (1) or decreasing (-1)

    """
    return _movement_controller.get_speed()

def change_speed(new_value, increment):
    """  Changes the speed of movement for the controller

    Keyword Arguments:
    increment -- whether the speed is increasing (1) or decreasing (-1)

    """
    _movement_controller.speed_change(new_value, increment)

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

# Feed start and stop commands stubbed for now as 
# live streaming is on hold for more critical features.

def __work(main_field):
    """ Initialized camera feed 
    Exists due to an oddity in python threading
    Corresponding facade handler removed for the moment"""
    # main_field.start_camera_feed()
    pass

def start_feed(main_field):
    """ Start new thread for camera window """
    #p = Process(target=__work, args=(main_field,))
    #p.start()
    #t = threading.Thread(target=__work, args=(main_field,))
    #t.start()

def stop_feed(main_field):
    """ Signal camera thread to stop """
    #main_field.stop_camera_feed()

def get_frame_np(main_field):
    """ Get a numpy array frame to display in the main window """
    #return np.asarray(main_field.get_plain_frame())
