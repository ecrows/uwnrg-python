from heapq import heappush, heappop
from aStarNode import *

#computes the A* path finding algorithm between two points
def AStar(grid_map,
          x_size,
          y_size,
          x_directions,
          y_directions,
          x_start,
          y_start,
          x_end,
          y_end):

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
    n0 = AStarNode(x_start, y_start, 0, 0)
    n0.updateScore(x_end, y_end)
    heappush(open_queue[o_q_index], n0)
    open_nodes[y_start][x_start] = n0.score

    while len(open_queue[o_q_index]) > 0:
        n1 = open_queue[o_q_index][0]
        n0 = AStarNode(n1.x_position,
                       n1.y_position,
                       n1.total_distance,
                       n1.score)
        x = n0.xPosition
        y = n0.yPosition
        heappop(open_queue[o_q_index])
        open_nodes[y][x] = 0
        closed_nodes[y][x] = 1

        #if the current position has hit the target position
        if x == x_end and y == y_end:
            #Store off the directions by retracing over the direction map
            path = ''
            while not (x == x_start and y == y_start):
                j = direction_history[y][x]
                c = str((j + 4) % 8)
                path = c + path
                x += x_directions[j]
                y += y_directions[j]

            #return the final path
            return path


        #loop through the direction choices
        for i in range(8):

            #grab the next cell index in the selected direction
            xdx = x + x_directions[i]
            ydy = y + y_directions[i]

            #If the position is not outside of the grid, the position is not a
            #wall, and the position has not been handled..
            if not (xdx < 0 or xdx > x_size - 1 or ydy < 0 or ydy > y_size - 1
                    or grid_map[ydy][xdx] == 1 or closed_nodes[ydy][xdx] == 1):

                #Make a node
                m0 = AStarNode(xdx, ydy, n0.total_distance, n0.score)

                #Perform distance calculation and set score
                m0.adjustDistance(i)
                m0.updateScore(x_end, y_end)

                #If the open map element has not been set,
                #set it and update the direction map
                if open_nodes[ydy][xdx] == 0:
                    open_nodes[ydy][xdx] = m0.score
                    heappush(open_queue[o_q_index], m0)

                    #Want to store the reverse direction,
                    #for ease of processing later.
                    direction_history[ydy][xdx] = (i + 4) % 8

                #We also process if the new node has a better score
                elif open_nodes[ydy][xdx] > m0.score:
                    open_nodes[ydy][xdx] = m0.score

                    #Want to store the reverse direction,
                    #for ease of processing later.
                    direction_history[ydy][xdx] = (i + 4) % 8
                    while not (open_queue[o_q_index][0].x_position == xdx
                               and open_queue[o_q_index][0].y_position == ydy):
                        heappush(open_queue[1 - o_q_index],
                                 open_queue[o_q_index][0])
                        heappop(open_queue[o_q_index])

                    heappop(open_queue[o_q_index])

                    if len(open_queue[o_q_index]) >
                       len(open_queue[1 - o_q_index]):
                        o_q_index = 1 - o_q_index

                    while len(open_queue[o_q_index]) > 0:
                        heappush(open_queue[1-o_q_index],
                                 open_queue[o_q_index][0])
                        heappop(open_queue[o_q_index])

                    o_q_index = 1 - o_q_index
                    heappush(open_queue[o_q_index], m0)

    #No path found, so return empty route
    return ''
