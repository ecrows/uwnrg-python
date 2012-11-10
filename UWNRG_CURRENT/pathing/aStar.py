# UWaterloo Nano Robotics Group
# A* Path Finding Algorithm

from heapq import heappush, heappop
from aStarNode import *

#computes the A* path finding algorithm between two points
def AStar(gridMap, xSize, ySize, xDirections, yDirections, xStart, yStart, xEnd, yEnd):

    #Handled nodes
    closedNodes = [] 

    #Unhandled nodes
    openNodes = []

    #Directions taken
    directionHistory = []


    #Fill maps with empty rows in each column
    row = [0] * xSize
    for i in range(ySize):
        closedNodes.append(list(row))
        openNodes.append(list(row))
        directionHistory.append(list(row))


    openQueue = [[], []]
    oQIndex = 0

    #Create and store the starting node
    n0 = AStarNode(xStart, yStart, 0, 0)
    n0.updateScore(xEnd, yEnd)
    heappush( openQueue[oQIndex], n0)
    openNodes[yStart][xStart] = n0.score

    while len(openQueue[oQIndex]) > 0:
        n1 = openQueue[oQIndex][0] 
        n0 = AStarNode(n1.xPosition, n1.yPosition, n1.totalDistance, n1.score)
        x = n0.xPosition
        y = n0.yPosition
        heappop(openQueue[oQIndex]) 
        openNodes[y][x] = 0
        closedNodes[y][x] = 1 

        #if the current position has hit the target position
        if x == xEnd and y == yEnd:
            
            #Store off the directions by retracing over the direction map
            path = ''
            while not (x == xStart and y == yStart):
                j = directionHistory[y][x]
                c = str((j + 4) % 8)
                path = c + path
                x += xDirections[j]
                y += yDirections[j]

            #return the final path
            return path


        #loop through the direction choices
        for i in range(8):

            #grab the next cell index in the selected direction
            xdx = x + xDirections[i]
            ydy = y + yDirections[i]

            #If the position is not outside of the grid, the position is not a wall, and the position has not been handled..
            if not (xdx < 0 or xdx > xSize-1 or ydy < 0 or ydy > ySize - 1 or gridMap[ydy][xdx] == 1 or closedNodes[ydy][xdx] == 1):

                #Make a node
                m0 = AStarNode(xdx, ydy, n0.totalDistance, n0.score)

                #Perform distance calculation and set score
                m0.adjustDistance(i)
                m0.updateScore(xEnd, yEnd)

                #If the open map element has not been set, set it and update the direction map
                if openNodes[ydy][xdx] == 0:
                    openNodes[ydy][xdx] = m0.score
                    heappush(openQueue[oQIndex], m0)
                    directionHistory[ydy][xdx] = (i + 4) % 8 #Want to store the reverse direction, for ease of processing later.

                #We also process if the new node has a better score
                elif openNodes[ydy][xdx] > m0.score:
                    openNodes[ydy][xdx] = m0.score
                    directionHistory[ydy][xdx] = (i + 4) % 8 #Want to store the reverse direction, for ease of processing later.

                    while not (openQueue[oQIndex][0].xPosition == xdx and openQueue[oQIndex][0].yPosition == ydy):
                        heappush(openQueue[1 - oQIndex], openQueue[oQIndex][0])
                        heappop(openQueue[oQIndex])

                    heappop(openQueue[oQIndex])

                    if len(openQueue[oQIndex]) > len(openQueue[1 - oQIndex]):
                        oQIndex = 1 - oQIndex

                    while len(openQueue[oQIndex]) > 0:
                        heappush(openQueue[1-oQIndex], openQueue[oQIndex][0])
                        heappop(openQueue[oQIndex])      

                    oQIndex = 1 - oQIndex
                    heappush(openQueue[oQIndex], m0)
    
    #No path found, so return empty route
    return ''