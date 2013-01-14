class Field:
    """
    Contains methods for each field.
    
    """
    
    # Region of interest that we're limiting processing to
    # This saves time and lets us avoid any borders
    roi_top = -1
    roi_bot = -1
    roi_left = -1
    roi_right = -1

    def _show_boundaries(self, image, leftline, rightline, botline, topline):
        """ Draw rectangular boundaries on image specified by 'image'.
        Currently hardcoded for a rectangular field.

        Should be implemented by child.

        #TODO: Should eventually take *lines* as input, not horiz/vert index.

        Keyword Arguments:
        image -- image to draw boundaries on
        leftline -- leftline is the x co-ordinate of the vertical left line
        rightline -- rightline is the x co-ordinate of the vertical right line
        botline -- botline is the y co-ordinate of the horizontal left line
        topline -- topline is the y co-ordinate of the horizontal left line
        """
        raise NotImplementedError

    def __init__(self, height=32, width=32):
        """ Initializes the Field Type

        Keyword Arguments:
        height -- height of the array representing the field
        width -- width of the array representing the field

        """
        self.GRID_H = height
        self.GRID_W = width

    def find_field(self, frame):
        """Returns array representation of rectangular field. Should be called
        *once* at the beginning of the challenge. Works only on an aligned
        vertically and horizontally field.

        Should be implemented by child.

        Keyword Arguments:
        frame -- The camera frame to analyze

        """
        raise NotImplementedError

    def find_robot(self, frame):
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
        raise NotImplementedError

    def _find_rect_boundary(self, edges, type):
        """Find the edges of a rectangular field and return line index

        Should only be called *once* at the beginning of the challenge
        Pretty hack-y way to clean up the find_eight_field method

        #TODO: Make this less disgusting.

        Keyword Arguments:
        edges -- a list of all possible edges
        type -- the type of edge to find

        """
        linedex = -1
        detail=10       # look at every tenth pixel
        thresh=8        # must have at least 8 pixels to match
        rowcount = 0

        if type == "bottom":
            for rows in edges:
                count = 0
                i = 0

                while i < rows.size:
                    if rows[i]==255:
                        count+=1

                    i+=detail

                if count > thresh:
                    linedex = rowcount

                rowcount+=1
        elif type == "top":
            for rows in edges:
                count = 0
                i = 0

                while i < rows.size:
                    if rows[i]==255:
                        count+=1

                    i+=detail

                if count > thresh:
                    linedex = rowcount
                    break

                rowcount+=1
        elif type == "right":
            for rows in edges.T:
                count = 0
                i = 0

                while i < rows.size:
                    if rows[i]==255:
                        count+=1

                    i+=detail

                if count > thresh:
                    linedex = rowcount

                rowcount+=1
        elif type == "left":
            for rows in edges.T:
                count = 0
                i = 0

                while i < rows.size:
                    if rows[i]==255:
                        count+=1

                    i+=detail

                if count > thresh:
                    linedex = rowcount
                    break

                rowcount+=1
        else:
            return -1

        return linedex

