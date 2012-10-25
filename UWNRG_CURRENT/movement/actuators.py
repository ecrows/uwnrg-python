import log as log
import movement.controller as controller

class Actuators(controller.Controller):

    def move_immediate(self, vector, invert_x_axis, invert_y_axis):
        """ Given input parameters, moves the robot appropriately

        Keyword Arguments:
        self -- actuator object the function was called on
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """

        flip_dict = [1,1,1]

        if invert_x_axis:
            #prepares the x and rotation direction to be flipped
            flip_dict = tuple(i * j for i, j in zip(flip_dict, [-1, 1, -1]))

        if invert_y_axis:
            #prepares the y and rotation direction to be flipped
            flip_dict = tuple(i * j for i, j in zip(flip_dict, [1, -1, -1]))

        vector = tuple(i * j for i, j in zip(flip_dict, vector))

        log.log_info("Move Immediate - VECTOR: " + str(vector))
