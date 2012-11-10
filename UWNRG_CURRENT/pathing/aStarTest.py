# UWaterloo Nano Robotics Group
# A* Path Finding Algorithm

import time
from aStar import *
from random import randint

#Configure the direction vectors - 8 different directions since we can move diagonally
xDirections = [1, 1, 0, -1, -1, -1, 0, 1]
yDirections = [0, 1, 1, 1, 0, -1, -1, -1]

#Configure the size of the map
xSize = 32
ySize = 32

#Create the map itself
gridMap = []

#insert a bunch of empty rows into the columns of the map
row = [0] * xSize
for i in range(ySize):
    gridMap.append(list(row))

#add some obstacles - this makes a "plus" shape in the center
for x in range(xSize / 8, xSize * 7 / 8):
    gridMap[ySize / 2][x] = 1
for y in range(ySize/8, ySize * 7 / 8):
    gridMap[y][xSize / 2] = 1

#add some more random obstacles
for z in range(0,80):
    gridMap[randint(0,xSize-1)][randint(0,ySize-1)] = 1

#set starting and ending points to map
(xStart, yStart, xEnd, yEnd) = (0,0, randint(0,xSize-1), randint(0,ySize-1))


#time and perform the A* algorithm
t = time.time()
route = AStar(gridMap, xSize, ySize, xDirections, yDirections, xStart, yStart, xEnd, yEnd)
print 'Time to generate the path: ', time.time() - t


#if a valid route was returned
if len(route) > 0:

    #flag the start position index
    x = xStart
    y = yStart
    gridMap[y][x] = 2

    #loop over the route and set the map indices to the Route setting
    for i in range(len(route)):
        j = int(route[i])
        x += xDirections[j]
        y += yDirections[j]
        gridMap[y][x] = 3

    #flag the end position index
    gridMap[y][x] = 4



print 'Final Grid:'
for y in range(ySize):
    for x in range(xSize):
        gridElement = gridMap[y][x]
        if gridElement == 0:
            print '-', # open space
        elif gridElement == 1:
            print ' ', # wall
        elif gridElement == 2:
            print 'S', # start position
        elif gridElement == 3:
            print '*', # route location
        elif gridElement == 4:
            print 'E', # end position

    print ''