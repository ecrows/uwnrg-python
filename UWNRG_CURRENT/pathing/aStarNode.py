import math

#The node class for the path finder
class AStarNode:

    #X Position of the node
    xPosition = 0.0

    #Y Position of the node
    yPosition = 0.0

    #Total distance traveled thus far
    totalDistance = 0.0

    #Score for evaluating the node
    score = 0.0

    #initialize the node
    def __init__(self, xPosition, yPosition, totalDistance, score):
        self.xPosition= xPosition
        self.yPosition = yPosition
        self.totalDistance = totalDistance
        self.score = score


    #comparator for score values, used by the queue
    def __lt__(self, other):
        return self.score < other.score


    #update node score
    def updateScore(self, xDest, yDest):
        #score is set based on the node's current
        #distance and the estimated distance heuristic
        self.score = self.totalDistance + self.distEst(xDest, yDest)


    #Adjust total distance in the direction
    def adjustDistance(self, directionIndex): 
        #If the direction is along a diagonal...
        if directionIndex % 2 != 0:
            #increment the traveled distance by sqrt(2), a.k.a ~1.5
            self.totalDistance += 1.5
        else:
            #increment by a standard edge length, 1
            self.totalDistance += 1.0


    #estimates the distance between the current position and the destination
    #using a standard linear difference
    def distEst(self, xDest, yDest):
        xd = xDest - self.xPosition
        yd = yDest - self.yPosition

        d = math.sqrt(xd * xd + yd * yd)

        return d
