import time
import pathing.astar as astar
import random as random

#Configure the size of the map
x_size = 32
y_size = 32

#Create the map itself
grid_map = []
row = [0] * x_size
for i in range(y_size):
    grid_map.append(list(row))

#add some obstacles - this makes a "plus" shape in the center
for x in range(x_size / 8, x_size * 7 / 8):
    grid_map[y_size / 2][x] = 1
for y in range(y_size/8, y_size * 7 / 8):
    grid_map[y][x_size / 2] = 1

#add some more random obstacles
for z in range(0, 80):
    grid_map[random.randint(0, y_size - 1)][random.randint(0, x_size - 1)] = 1

#set starting and ending points to map
(x_start, y_start, x_end, y_end) = (0,
                                    0,
                                    random.randint(0, x_size - 1),
                                    random.randint(0, y_size - 1))

#ensure stop is not on an obstacle
while (grid_map[y_end][x_end] == 1):
    (x_end, y_end) = (random.randint(0, x_size - 1),
                      random.randint(0, y_size - 1))

#time and perform the A* algorithm
t = time.time()
pathing = astar.AStar()
route = pathing.calculate_route(grid_map,
              x_start,
              y_start,
              x_end,
              y_end)
print 'Time to generate the path: ', time.time() - t

#flag the start position index
x = x_start
y = y_start
grid_map[y][x] = 2

#if a valid route was returned
if len(route) > 0:
    #loop over the route and set the map indices to the Route setting
    for i in route:
        x += i[0]
        y += i[1]
        grid_map[y][x] = 3

#flag the end position index
grid_map[y_end][x_end] = 4

print 'Final Grid:'
for y in range(y_size):
    for x in range(x_size):
        grid_element = grid_map[y_size-1-y][x]

        # open space
        if grid_element == 0:
            print '.',
        # wall
        elif grid_element == 1:
            print 'X',
        # start position
        elif grid_element == 2:
            print 'S',
        # route location
        elif grid_element == 3:
            print 'O',
        # end position
        elif grid_element == 4:
            print 'E',

    print ''