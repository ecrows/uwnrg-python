"""Image Recognition Module

Field-specific recognition methods are called before starting movement.
Robot-finding method should be called during runtime.
Triangle finding (when implemented) will be good.

Performance Note:
Frames must be processed within 0.033 to make
the 30 FPS camera the bottleneck.
A small testing app I wrote puts the average filtering time per image
at 0.015 per frame.  That means the robot finding algorithm has about
0.018 seconds to run - plenty of time, especially if we preprocess
the field (which Dule says we can).

TODO: Implement getters and setters for thresholding values etc.
TODO: Analyze code to make sure that it follows style guidelines.
TODO: Compensate for field angle skew?

Questions/comments/concerns/requests? Bug Evan.

"""

import cv2 as cv2
import numpy as np
import figure_eight as figure_eight
import micro_assembly as micro_assembly

class ImageRecognition:
    # Type of field/challenge being performed
    # 0 = Figure Eight
    # 1 = Micro Assembly
    ftype = 0

    def __init__(self, type="eight"):
        self.set_field_type(type)

        pass

    def set_field_type(self, type):
        if (type == "eight"):
            self.ftype = 0
        elif (type == "micro"):
            self.ftype = 1

    def new_field(self):
        """Return field object of type "type"

        Use "eight" to refer to Figure8.
        Use "micro" to refer to MicroAssembly.

        """

        if (self.ftype == 0):
            return figure_eight.Figure8(frame)
        elif (self.ftype == 1):
            return micro_assembly.MicroAssembly(frame)
        else:
            # TODO: Make our own exception to raise here
            raise NameError("Invalid field type specified") 

    def find_field(self, frame):
        """Return array representation of rectangular field.
        Should be called *once* at the beginning of the challenge. Works only
        on an aligned vertically and horizontally field.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        self.fieldtype.find_field(frame)

    def find_robot(self, frame):
        """Finds the robot given a camera frame.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        self.fieldtype.find_robot(frame)
