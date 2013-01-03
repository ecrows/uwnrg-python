import field as field

class MicroAssembly(field.FieldType):
    def find_field(self, frame):
        """Returns array representation of rectangular field. Should be called
        *once* at the beginning of the challenge. Works only on an aligned
        vertically and horizontally field.

        #TODO: IMPLEMENT

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        pass

    def find_robot(self):
        """Finds the robot given a camera frame.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        """
        NOTES ON POSSIBLE IMPLEMENTATION:
        Solving this problem is likely going to be the most difficult
        part of this.

        Current plan:
        Was planning on saving the array of feature pixels on the first pass
        through, then making a pass along the y and x axis to add up the 
        feature pixels along each line.
        Any substantial increase of feature pixels at a particular x-y
        coordinate is indicative of the robot being at that location.

        The problem with this method is that the robot's initial position would
        leave a "blind spot" in the detection algorithm unless manually
        compensated for.

        Alternatively, I could save an array of feature pixels on each
        "find_robot" call. Then any increase in feature count would likely
        work.

        Further improvements to this strategy would probably be made through
        searching only areas of the field where the robot is likely to be.
        That is to say, aggressively mark around the outside boundaries and the
        middle walls and search between them for the largest clump of pixels
        (which should be the robot).

        Another question worth asking is whether the Canny filter setup
        currently used for wall detection is also the best way to detect the
        robot. There could easily exist a more conspicuous way to mark the
        robot out.
        """
        pass
