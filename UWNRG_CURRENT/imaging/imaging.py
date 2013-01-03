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

    def __init__(self, type="eight"):
        self.set_field_type(type)

    def set_field_type(self, type):
        """Set field type value

        Use "eight" to refer to Figure8.
        Use "micro" to refer to MicroAssembly.

        """

        if (type == "eight"):
            self.fieldtype = figure_eight.Figure8()
        elif (type == "micro"):
            self.fieldtype = micro_assembly.MicroAssembly()
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

    def process (self):
        """Testing harness to see what's going on"""
        vc = cv2.VideoCapture("MobilityRun1.wmv")
        rval, frame = vc.read()

        if (rval):
            testput = self.find_field(frame)
            np.set_printoptions(threshold='nan')
            print testput
