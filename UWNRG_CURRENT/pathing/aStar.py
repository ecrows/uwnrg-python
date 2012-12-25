import heapq as heapq
import math as math
import pathing as pathing
import copy as copy

class AStar(pathing.Pathing):
    """ pathing implementation for AStar """
    #x_directions[i] and y_directions[i] are used in conjuction to
    #create a direction vector
    #__x_directions = [1, 1, 0, -1, -1, -1, 0, 1]
    #__y_directions = [0, 1, 1, 1, 0, -1, -1, -1]
    __x_directions = [1, 0, -1, 0]
    __y_directions = [0, 1, 0, -1]

    def calculate_route(self, grid_map, x_start, y_start, x_end, y_end):
        """ Calculates the optimal route between two points using AStar

        Keyword arguments:
        grid_map -- 2D list, assumed to be rectangular in size. Represents the
                    field to navigate. 1 represents an obstacle, 0 represents
                    an open grid space
        x_start -- x position of the starting location
        y_start -- y position of the starting location
        x_end -- x position of the ending location
        y_end -- y position of the ending location

        """
        y_size = len(grid_map)
        x_size = len(grid_map[0])

        #Handled nodes
        closed_nodes = []

        #Unhandled nodes
        open_nodes = []

        #Directions taken
        direction_history = []

        #Fill maps with empty rows in each column
        row = [0] * x_size

        for i in range(y_size):
            closed_nodes.append(list(row))
            open_nodes.append(list(row))
            direction_history.append(list(row))

        open_queue = [[], []]
        o_q_index = 0

        #Create and store the starting node
        n0 = AStar._Node(x_start, y_start, x_end, y_end, 0)
        heapq.heappush(open_queue[o_q_index], n0)
        open_nodes[y_start][x_start] = n0.cost

        while len(open_queue[o_q_index]) > 0:
            n1 = open_queue[o_q_index][0]
            n0 = copy.deepcopy(n1)

            x = n0.x_position
            y = n0.y_position

            heapq.heappop(open_queue[o_q_index])

            open_nodes[y][x] = 0
            closed_nodes[y][x] = 1

            #if the current position has hit the target position
            if x == x_end and y == y_end:
                #Store off the directions by retracing over the direction map
                path = ''

                while not (x == x_start and y == y_start):
                    j = direction_history[y][x]
                    c = str((j + 4) % 8) #todo, figure out what this is
                    path = c + path
                    x += self.__x_directions[j]
                    y += self.__y_directions[j]

                #return the final path
                return path


            #loop through the direction choices
            for i in range(len(self.__x_directions)):
                #grab the next cell index in the selected direction
                xdx = x + self.__x_directions[i]
                ydy = y + self.__y_directions[i]

                #If the position is not outside of the grid, the position is
                #not a wall, and the position has not been handled..
                if not (xdx < 0 or
                        xdx > x_size - 1 or
                        ydy < 0 or ydy > y_size - 1 or
                        grid_map[ydy][xdx] == 1 or
                        closed_nodes[ydy][xdx] == 1):

                    #Make a node
                    m0 = AStar._Node(xdx,
                                     ydy,
                                     x_end,
                                     y_end,
                                     n0.distance + self.__travelled_distance(i))

                    #If the open map element has not been set,
                    #set it and update the direction map
                    if open_nodes[ydy][xdx] == 0:
                        open_nodes[ydy][xdx] = m0.cost
                        heapq.heappush(open_queue[o_q_index], m0)

                        #Want to store the reverse direction,
                        #for ease of processing later.
                        direction_history[ydy][xdx] = (i + 4) % 8 #TODO here again

                    #We also process if the new node has a better cost
                    elif open_nodes[ydy][xdx] > m0.cost:
                        open_nodes[ydy][xdx] = m0.cost

                        #Want to store the reverse direction,
                        #for ease of processing later.
                        direction_history[ydy][xdx] = (i + 4) % 8 #TODO WTF

                        while not (open_queue[o_q_index][0].x_position == xdx and
                                   open_queue[o_q_index][0].y_position == ydy):
                            heapq.heappush(open_queue[1 - o_q_index],
                                     open_queue[o_q_index][0])
                            heapq.heappop(open_queue[o_q_index])

                        heapq.heappop(open_queue[o_q_index])

                        if len(open_queue[o_q_index]) > \
                           len(open_queue[1 - o_q_index]):
                            o_q_index = 1 - o_q_index

                        while len(open_queue[o_q_index]) > 0:
                            heapq.heappush( open_queue[1-o_q_index],
                                            open_queue[o_q_index][0])
                            heapq.heappop(open_queue[o_q_index])

                        o_q_index = 1 - o_q_index
                        heapq.heappush(open_queue[o_q_index], m0)

        #No path found, so return empty route
        return ''

    def __travelled_distance(self, i):
        """ Returns the distance travelled as a result of the direction
            vector taken to get to the Node

        Keyword arguments:
        i -- direction index

        """
        if i is None:
            return 0
        else:
            return self.__x_directions[i] + self.__y_directions[i]

    class _Node:
        """ Used to represent nodes in the grid """
        def __init__(self,
                     x_position,
                     y_position,
                     x_dest,
                     y_dest,
                     distance):
            """ Initializes the Node

            Keyword arguments:
            x_position -- the x coordinate of the node
            y_position -- the y coordinate of the node
            x_dest -- x coordinate of the destination
            y_dest -- y coordinate of the destination
            distance -- the distance travelled to reach the node

            """
            self.__x_position = x_position
            self.__y_position = y_position
            self.__distance = distance
            self.__cost = self.__distance + self.__dist_est(x_dest, y_dest)

        def get_cost(self):
            """ Returns the cost of the Node """
            return self.__cost

        def get_distance(self):
            """ Returns the distanced travelled to reach the Node """
            return self.__distance

        def get_x_position(self):
            """ Returns the x position of the Node """
            return self.__x_position

        def get_y_position(self):
            """ Returns the x position of the Node """
            return self.__y_position

        cost = property(get_cost)
        distance = property(get_distance)
        x_position = property(get_x_position)
        y_position = property(get_y_position)

        def __lt__(self, other):
            """ Comparator for cost of each Node

            Keyword arguments:
            other -- Node to compare current Node to

            """
            return self.cost < other.cost

        def __dist_est(self, x_dest, y_dest):
            """ Generates a heuristic for the distance between the current
                position and the destination

            Keyword arguments:
            x_dest -- x coordinate of the destination
            y_dest -- y coordinate of the destination

            """
            xd = x_dest - self.x_position
            yd = y_dest - self.y_position

            d = math.sqrt(xd * xd + yd * yd)

            return d
