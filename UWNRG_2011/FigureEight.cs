//when finding the x value where it has a clear path up, to the next gap... might need to change depending on amount of false positives for walls
//can be done by checking for the percentage of walls inbetween the two, and come up with a threshold level.
//all proccesses dealing with the y coordinate are done in terms of the grid where up is a positive increase in the y-index value. since the top left is (0,0) moving up is actually a decrease in index value, so the final return is multiplied by -1 to return the proper direction of movement

//start is as a parameter in the main function because i'm expecting to get the location of the robot to start, right now it doesn't do anything and i just have the code find start based off the letter in the grid

//current code needed to recieve the optimal path
/* int [] start = new int [-1,-1]
FigureEight solution = new FigureEight();
solution.path = solution.GetOptimalPath(ref cameragrid, start);*/

using System;
using System.Collections.Generic;
namespace UWNRG_2011
{
    class FigureEight
    {
        private int SideofGap(ref char[,] cameraGrid, ref int[,] criticalPoints, int[,] gaps, int firstGap, int secondGap, int width) //finds the nearest coordinates of 2 spots on one side of a wall, with the gaps in it, which have no wall grid spaces in between them
        {
            int x, y;
            for (int xDirection = 1; xDirection >=-1; xDirection -= 2) //runs right and left side
            {
                for (x = gaps[firstGap, 1]; x < width && x >= 0; x += xDirection) //traverses away from the wall
                {
                    if (cameraGrid[gaps[firstGap, 0],x] == 'x' || cameraGrid[gaps[secondGap, 0],x] == 'x') //if it runs into a wall horizontal of the supposed gap
                    {
                        return (cameraGrid[gaps[firstGap, 0],x] == 'x'?firstGap:secondGap); //returns which gap isn't a proper gap
                    }
                    for (y = gaps[firstGap, 0]; y != gaps[secondGap, 0] && cameraGrid[y, x] != 'x'; y -= 1) //traverses between the temporary co-ordinates (originating from the gaps in the wall) checks if they are seperated vertically by wall grid spaces
                    {
                    }
                    if (cameraGrid[y, x] != 'x') //if no wall grid spaces were found between the temporary co-ordinates
                    {

                        /*
                             |      |            |      |
                            5 6    2 1           1      3               
                             |      |            |      |               
                            4 3    7 8           0      2               
                             |      |            |      |               
                    the critical points index   the gap index         
                        */
                        //sets x co-ordinates of critical points that can connect to each other vertically
                        if (firstGap < 2) //if working on the left side
                        {
                            if (xDirection == 1) //if on the right side of the wall
                            {
                                criticalPoints[6, 1] = criticalPoints[3, 1] = x;
                            }
                            else //if on the left side of the wall
                            {
                                criticalPoints[5, 1] = criticalPoints[4, 1] = x;
                            }
                        }
                        else // if working on the right side
                        {
                            if (xDirection == 1) //if on the right side of the wall
                            {
                                criticalPoints[1, 1] =  criticalPoints[8, 1] = x;
                            }
                            else //if on the left side of the wall
                            {
                                criticalPoints[2, 1] = criticalPoints[7, 1] = x;
                            }
                        }
                        break;
                    }
                }
            }
            //relationship: (3+2*gap)%8 gives 1,3,5,7
            //sets y co-ordinates of the gaps
            criticalPoints[(3 + 2 * firstGap) % 8, 0] = criticalPoints[(3 + 2 * firstGap) % 8 + 1, 0] =gaps[firstGap, 0] ;
            criticalPoints[(3 + 2 * secondGap) % 8, 0] = criticalPoints[(3 + 2 * secondGap) % 8 + 1, 0] = gaps[secondGap, 0];
            return 4; //if no error and found a possible gap
        }
        /// <summary>
        /// An list of arrays. The arrays contain the components [x,y]. X being the horizontal component of movement and y the vertical.
        /// These are direction vectors for the robot to take to traverse the grid in the shortest distance possible.
        /// </summary>
        public List<int[]> path = new List<int[]>(); //global variable for the path to be followed   
        /// <summary>
        /// Takes in an array representing the playing field. 'x' for wall, 'o' for open. Can also take in the starting position if known.
        /// Returns the path variable of the figure eight class.
        /// </summary>
        /// <param name="cameraGrid"></param>
        /// <param name="start"></param>
        /// <returns></returns>
        public List<int[]> GetOptimalPath(ref char[,] cameraGrid, int[] start) //finds the path to be taken to traverse the figure eight playing field
        {
            int height = cameraGrid.GetLength(0), width = cameraGrid.GetLength(1); //size of the grid
            start = FindLocation(ref cameraGrid,start); //checks if the start position has been entered, if not it finds it
            int[,] criticalPoints = GapSearch(ref cameraGrid, height, width); //sets the y,x coordinates for the gaps in the walls for the figure eight
            criticalPoints[0, 0] = start[0]; //sets the starting location
            criticalPoints[0, 1] = start[1];
            for (int i = 1; i < 9; i++) //finds the difference in the positions giving the direction vector needed to be taken
            {
                path.Add(new int[] { criticalPoints[i, 1] - criticalPoints[i - 1, 1], criticalPoints[i - 1, 0] - criticalPoints[i, 0] });//flipped the y-coordinate around because the position on the grid is inverted (a positive movement in the grid is a negative in real life) due the (0,0) being the top left
            }
            return path;
        }
        private int GapInY(ref char[,] cameraGrid, int x, int y, int gap,int height) //checks for gap in wall (y co-ordinate)
        {
            bool prevOpen = false; //used to give buffer from wall (can get rid of and it will choose the next wall (however would have to add 1 to the x value given by the recheck function call)
            int yDirection; //determines if it needs to check upwards or down from the given spot for the gap
            if (gap % 2 == 0)
            {
                yDirection = 1;
            }
            else
            {
                yDirection = -1;
            }
            for (; y < height && y >= 0; y += yDirection) //checks for a gap of size 2
            {
                if (cameraGrid[y, x] != 'x')
                {
                    if (prevOpen == false) //if previous was a wall
                    {
                        prevOpen = true;
                    }
                    else
                    {
                        return y;
                    }
                }
            }
            Console.WriteLine("ERROR, could not find open y."); //if there were no y that satisfied the conditions of the gap
            return -1; //if an error
        }
        private int[,] GapSearch(ref char[,] cameraGrid, int height, int width) //searches for the gaps in the wall
        {
            int midX = width / 2 - 1, //stores the middle x value
                midY = height / 2 - 1; //stores the middle y value
            int[,] yxPositions = new int[9, 2]; //stores the y and x values (in that order) of the gaps in the wall
            int[,] gaps = new int[4, 2]; //stores the y and x values (in that order) of the gaps in the wall
            int []tempGap= new int[2]; //temporarily stores the value of a possible gap
            int findGap;
            for (int xDirection = 1; xDirection >=-1; xDirection -= 2) //runs left and right side
            {
                findGap = 0;
                gaps[1 - xDirection, 1] = gaps[2 - xDirection, 1] = XSearch(ref cameraGrid, midX, width, height, xDirection); //finds the x value for both gaps on the side that was just checked
                gaps[1 - xDirection, 0] = GapInY(ref cameraGrid, gaps[1 - xDirection, 1], midY, 1 - xDirection, height); //finds the first bottom gap possible on the current side
                gaps[2 - xDirection, 0] = GapInY(ref cameraGrid, gaps[2 - xDirection, 1], midY, 2 - xDirection, height); //finds the first top gap possible on the current side
                while (findGap!= 4) //until a proper gap is found
                {
                    findGap = SideofGap(ref cameraGrid, ref yxPositions, gaps, 1 - xDirection, 2 - xDirection, width); //finds gap or sets findGap to the index value of the gap that needs to be fixed
                    if (findGap!= 4) //if not a proper gap
                    {
                        gaps[findGap,0] = GapInY(ref cameraGrid, gaps[findGap,1], gaps[findGap,0], findGap, height); //checks for next possible gap on the side being checked
                    }
                }
            }
            return yxPositions;
        }
        private int XSearch(ref char[,] cameraGrid, int middle,int width,int height,int xDirection) //finds the x value of the gaps
        {
            int count;
            int threshold = 2*height/5; //arbitrary value that can be adjusted for better performance
            for (int x = middle; x>=0&&x<width; x -= xDirection) //runs through from the middle to the outside of the grid, therefore reading the wall with gaps in it before the outer edge wall
            {
                count = 0;
                for (int y = 0; y < height; y ++) //checks how many wall grid spaces there are in the column
                {
                    if (cameraGrid[y, x] == 'x') //if a wall grid space is found
                    {
                        count +=1;
                    }
                }
                if (count >= threshold) //if there are more wall spaces than normal, it must be a wall
                {
                    return x;
                }
            }
            Console.WriteLine("XSearch error");
            return -1; //only reaches this if an error occurs in the search
        }
        private int[] FindLocation(ref char[,] cameraGrid,int[] start) //finds the location of start if not already set
        {
            if (start[0] == -1 && start[1] == -1)//if either start or end does not have a value
            {
                for (int i1 = 0; i1 < cameraGrid.GetLength(0); i1++)//runs through height of cameraGrid
                {
                    for (int i2 = 0; i2 < cameraGrid.GetLength(1); i2++)//runs through width of cameraGrid
                    {
                        if ('s' == cameraGrid[i1, i2])//if it's the value being looked for
                        {
                            return new int[] { i1, i2 }; //returns the position of start
                        }
                    }
                }
            }
            return start; //already has the correct value
        }
    }
}