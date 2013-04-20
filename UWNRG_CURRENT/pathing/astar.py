import copy as copy
import heapq as heapq
import math as math
import pathing as pathing

class AStar(pathing.Pathing):
    """ pathing implementation for AStar """
    #possible direction vectors from the node (x,y)
    __direction_vectors = ((1,0),(0,1),(-1,0),(0,-1))

    def calculate_route(self, grid_map, x_start, y_start, x_dest, y_dest):
        """ Calculates the optimal route between two points using AStar

        Keyword arguments:
        grid_map -- 2D list, assumed to be rectangular in size. Represents the
                    field to navigate. 1 represents an obstacle, 0 represents
                    an open grid space
        x_start -- x position of the starting location
        y_start -- y position of the starting location
        x_dest -- x position of the destination
        y_dest -- y position of the destination

        """
        y_size = len(grid_map)
        x_size = len(grid_map[0])

        #Set of handled nodes
        closed_nodes = set()

        #Heap of unhandled nodes
        open_nodes = []

        #Map of navigated nodes
        came_from = {}

        #Create destination node for use as a reference
        dest_node = AStar._Node(x_dest, y_dest)

        #Create and store the starting node
        start_node = AStar._Node(x_start, y_start)
        start_node.set_distance_cost(dest_node, None)
        came_from[str(start_node.position)] = None
        closed_nodes.add(str(start_node.position))
        heapq.heappush(open_nodes, start_node)

        while len(open_nodes) > 0:
            current_node = heapq.heappop(open_nodes)

            #if the current position has hit the target position
            if current_node == dest_node:
                return self.__reconstruct_path(came_from, current_node)

            #loop through the direction choices
            for vector in self.__direction_vectors:
                temp_node = AStar._Node(current_node.x_position + vector[0],
                                        current_node.y_position + vector[1])

                #If the Node has not been visited, is within the grid and is
                #not an obstacle
                if (str(temp_node.position) not in closed_nodes and
                    temp_node.x_position >= 0 and
                    temp_node.x_position < x_size and
                    temp_node.y_position >= 0 and
                    temp_node.y_position < y_size and
                    grid_map[temp_node.y_position][temp_node.x_position] != 1):

                    temp_node.set_distance_cost(dest_node, current_node)
                    came_from[str(temp_node.position)] = current_node
                    closed_nodes.add(str(temp_node.position))
                    heapq.heappush(open_nodes, temp_node)

        #No path found, so return empty route
        return []


    def __reconstruct_path(self, came_from, current_node):
        """ Returns a list of direction vectors that give the shortest path
        from the start to the destination

        Keyword arguments:
        came_from -- dictionary of Nodes, where the key is the current Node,
                     and the value is the Node visited before it
        current_node -- the current Node being added to the path

        """
        if came_from[str(current_node.position)] is None:
            return []
        else:
            previous_node = came_from[str(current_node.position)]
            return self.__reconstruct_path(came_from, previous_node) + \
                    [(current_node - previous_node)]

    class _Node:
        """ Used to represent nodes in the grid """
        def __init__(self, x_position, y_position):
            """ Initializes the Node

            Keyword arguments:
            x_position -- the x coordinate of the node
            y_position -- the y coordinate of the node

            """
            self.__position = {}
            self.__position['x'] = x_position
            self.__position['y'] = y_position

        def set_distance_cost(self, dest_node, prev_node):
            """ Sets the distance and cost of the Node

            Keyword arguments:
            dest_node -- node containing the destination Node's coordinates
            prev_node -- node visited before current Node

            """
            if prev_node is None:
                self.__distance = 0
            else:
                self.__distance = prev_node.distance + \
                                  self.__dist_est(prev_node)

            self.__cost = self.__distance + self.__dist_est(dest_node)

        #properties
        cost = property(lambda self: self.__cost)
        distance = property(lambda self: self.__distance)
        x_position = property(lambda self: self.__position['x'])
        y_position = property(lambda self: self.__position['y'])
        position = property(lambda self: self.__position)

        def __lt__(self, other):
            """ Comparator for cost of each Node

            Keyword arguments:
            other -- Node to compare current Node to

            """
            if self.cost < other.cost:
                return True
            elif self.cost == other.cost:
                return self.distance < other.distance
            else:
                return False

        def __sub__(self, other):
            """ Subtraction operator

            Keyword arguments:
            other -- Node to subtract from current Node

            """
            return (self.x_position - other.x_position,
                    self.y_position - other.y_position)

        def __eq__(self, other):
            """ Equality operator

            Keyword arguments:
            other -- Node to subtract from current Node

            """
            return self.position == other.position

        def __dist_est(self, dest_node):
            """ Generates a heuristic for the distance between the current
                position and the destination

            Keyword arguments:
            dest_node -- node containing the destination Node's coordinates

            """
            return abs(math.fsum(self - dest_node))
