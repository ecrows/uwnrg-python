//may need to get rid of diagonal movement in this situation
//all proccesses dealing with the y coordinate are done in terms of the grid where up is a positive increase in the y-index value. since the top left is (0,0) moving up is actually a decrease in index value, so the final return is multiplied by -1 to return the proper direction of movement

// o _ o
// x x _
// x x o

//start and end are parameters in the main function because i'm expecting to get the location of the robot to start, right now it doesn't do anything and i just have the code find start and end based off the letters in the grid

//current code needed to recieve the optimal path
/* int [] start = new int [-1,-1]
Astar solution = new Astar();
solution.path = solution.GetOptimalPath(cameragrid, start,end)*/


using System;
using System.Collections.Generic;

namespace UWNRG_2011
{
    class Astar
    {
        /// <summary>
        /// An list of arrays. The arrays contain the components [x,y]. X being the horizontal component of movement and y the vertical.
        /// These are direction vectors for the robot to take to traverse the grid in the shortest distance possible.
        /// </summary>
        public List<int[]> path = new List<int[]>(); //global variable for the path to be followed
        private bool IsInside(int maxp, int p)//makes sure the point being checked is inside the grid
        {
            if (p >= 0 && p < maxp)//if inside the boundary returns true
            {
                return true;
            }
            return false;//otherwise returns false
        }
        public struct Node
        {
            char areaType;
            double distanceTravelled;
            double heuristic;
            int[] previousPathNode;
            bool isCorner;
            public char AreaType //whether it is a wall, start, end, open spot
            {
                get
                {
                    return areaType;
                }
                set
                {
                    areaType = value;
                }
            }
            public bool IsCorner //if the node is a corner
            {
                get
                {
                    return isCorner;
                }
                set
                {
                    isCorner = value;
                }
            }
            public double DistanceTravelled //distance travelled from the start node to this node
            {
                set
                {
                    distanceTravelled = value;
                }
                get
                {
                    return distanceTravelled;
                }
            }
            public double Heuristic //distance between node and the end node
            {
                set
                {
                    heuristic = value;
                }
            }
            public int[] PreviousPathNode //previous node in the path
            {
                get
                {
                    return previousPathNode;
                }
                set
                {
                    previousPathNode = value;
                }
            }
            public double Distance //returns the distance value used in A-star
            {
                get
                {
                    return heuristic + distanceTravelled;
                }
            }
        }
        private bool CornerCheck(int[] neighbourWalls)//checks the adjacent squares to see if the point is a corner
        {
            /* 0 1 2
               3   5
               6 7 8

            possible combinations:
                wall     wall     wall   not wall not wall
             *    1   |    0   |    3   |        |        |
             *    1   |    2   |    5   |        |        | 
             *    7   |    8   |    5   |        |        | 
             *    7   |    6   |    3   |        |        | 
             *    
             *    7   |        |        |    8   |    6   | 
             *    5   |        |        |    2   |    8   | either or both
             *    3   |        |        |    0   |    6   | 
             *    1   |        |        |    0   |    2   | 
             *    
             *    0   |        |        |    1   |    3   | 
             *    2   |        |        |    1   |    5   |  both
             *    6   |        |        |    7   |    3   | 
             *    8   |        |        |    7   |    5   |  
            */


            if (neighbourWalls[1] == 1)
            {
                if (neighbourWalls[0] == 1 && neighbourWalls[3] == 1)
                {
                    return true;
                }
                else if (neighbourWalls[2] == 1 && neighbourWalls[5] == 1)
                {
                    return true;
                }
                else if (neighbourWalls[0] == 0 || neighbourWalls[2] == 0)
                {
                    return true;
                }
            }
            if (neighbourWalls[7] == 1)
            {
                if (neighbourWalls[8] == 1 && neighbourWalls[5] == 1)
                {
                    return true;
                }
                else if (neighbourWalls[6] == 1 && neighbourWalls[3] == 1)
                {
                    return true;
                }
                else if (neighbourWalls[8] == 0 || neighbourWalls[6] == 0)
                {
                    return true;
                }
            }
            if (neighbourWalls[5] == 1)
            {
                if (neighbourWalls[2] == 0 || neighbourWalls[8] == 0)
                {
                    return true;
                }
            }
            if (neighbourWalls[3] == 1)
            {
                if (neighbourWalls[0] == 0 || neighbourWalls[6] == 0)
                {
                    return true;
                }
            }
            if (neighbourWalls[7] == 0)
            {
                if (neighbourWalls[3] == 0 && neighbourWalls[6] == 1)
                {
                    return true;
                }
                if (neighbourWalls[5] == 0 && neighbourWalls[8] == 1)
                {
                    return true;
                }
            }
            if (neighbourWalls[1] == 0)
            {
                if (neighbourWalls[3] == 0 && neighbourWalls[0] == 1)
                {
                    return true;
                }
                if (neighbourWalls[5] == 0 && neighbourWalls[2] == 1)
                {
                    return true;
                }
            }
            return false;
        }
        /// <summary>
        /// Takes in an array representing the playing field. 'x' for wall, 'o' for open. Can also take in the starting or end position if known.
        /// Returns the path variable of the figure eight class.
        /// </summary>
        /// <param name="cameraGrid"></param>
        /// <param name="start"></param>
        /// <param name="end"></param>
        /// <returns></returns>
        public List<int[]> GetOptimalPath(char[,] cameraGrid, int[] start, int[] end)
        {
            DateTime startingTime = new DateTime();
            startingTime = DateTime.Now;
            int height = cameraGrid.GetLength(0), width = cameraGrid.GetLength(1); //size of the grid
            bool firstAdded; //checks if it's the first node added to the heap
            FindLocation(cameraGrid,ref start,ref end);//checks if the start and end position have been entered, if not it finds them
            Node[,] grid = MakeArray(cameraGrid); //stores information for all the different areas on the grid

            List<int[]> heap = new List<int[]>(), //min-heap for next node to check
                tempPath = new List<int[]>(); //temporarily stores the path in a backwards order
            heap.Add(start); //starts searching from the start

            grid[start[0], start[1]].DistanceTravelled = 0; //sets information for starting node in grid
            grid[start[0], start[1]].Heuristic = Math.Sqrt(Math.Pow(start[0] - end[0], 2) + Math.Pow(start[1] - end[1], 2));
            grid[start[0], start[1]].IsCorner = true;
            grid[start[0], start[1]].PreviousPathNode = start;

            int[] neighbourWalls, //stores which neighbouring nodes are corners
                tempPreviousPathNode, //stores temporarily the previous node in the path
                tempPreviousCheckNode, //stores temporarily the previously checked node
                previousPathDirection, //will be used to combine direction vectors that are scalar multiples (occurs at the end of Astar)
                currentNode = heap[0]; //the current node being checked

            while (currentNode[0]!=end[0]||currentNode[1]!=end[1])//loops until the end point has been reached
            {
                firstAdded = true;
                neighbourWalls = new int[9];
                //currentNode = new int[] { 6, 8 };
                for (int y = -1; y < 2; y++)//check to see if node is a corner node or not
                {
                    for (int x = -1; x < 2; x++)
                    {
                        if (x != 0 || y != 0)//so that it doesn't check itself
                        {
                            if (grid[currentNode[0] + y, currentNode[1] + x].AreaType == 'x') //if the node is a wall
                            {
                                neighbourWalls[x + 4 - y * 3] = 1; //originally "x + 1 + (1 - y) * 3"
                            }
                        }
                    }
                }

                grid[currentNode[0], currentNode[1]].IsCorner = CornerCheck (neighbourWalls);

                for (int i = -1; i < 2; i++) //check for next spot to move to
                {
                    for (int j = -1; j < 2; j++)
                    {
                        if (i != 0 || j != 0)//so that it doesn't check itself
                        {
                            int x = currentNode[1] + j;
                            int y = currentNode[0] + i;
                            if (IsInside(height, y) && IsInside(width, x) && grid[y, x].AreaType != 'x')// checks if inside grid and not a wall
                            {
                                if (grid[y, x].DistanceTravelled != -1)// checks if it has been visited yet
                                {
                                    tempPreviousPathNode = grid[currentNode[0], currentNode[1]].IsCorner == true ? new int[] { currentNode[0], currentNode[1] } : grid[currentNode[0], currentNode[1]].PreviousPathNode; //if the previous node travelled is a corner, that's the previous path node, otherwise the previous path node of the previous node travelled is the previous node
                                    if (grid[y, x].DistanceTravelled > grid[tempPreviousPathNode[0], tempPreviousPathNode[1]].DistanceTravelled + Math.Sqrt(Math.Pow(y - tempPreviousPathNode[0], 2) + Math.Pow((x - tempPreviousPathNode[1]), 2))) //if the distance to that node is shorter than what was previously calculated
                                    {
                                        RevisitNode(ref grid, ref heap, x, y, tempPreviousPathNode[1], tempPreviousPathNode[0]);
                                    }
                                }
                                else  //hasn't been visited
                                {
                                    if (i * j != 0)//if trying to access corner where the two adjacent side positions are blocked
                                    {
                                        if (grid[y, currentNode[1]].AreaType == 'x' && grid[currentNode[0], x].AreaType == 'x')//checks if the adjacent edges are walls, in which case the corner is inaccessible
                                        {
                                            continue;
                                        }
                                    }
                                    firstAdded = AddToHeap(ref grid, x, y, end, firstAdded, ref heap, currentNode[0], currentNode[1]);
                                }
                            }
                        }
                    }
                }

                tempPreviousCheckNode = currentNode;
                currentNode = heap[0];

                if (tempPreviousCheckNode == currentNode)//if checking the same node again as no new nodes were added to the heap
                {
                    if (heap.Count == 1) //if this was the last possible node to check
                    {
                        Console.WriteLine(DateTime.Now - startingTime);
                        Console.WriteLine("No Possible Solution");
                        return path;
                    }
                    heap[0] = heap[heap.Count - 1]; //removes the node from the heap and fixes the heap
                    heap.RemoveAt(heap.Count - 1);
                    SortDown(ref grid, ref heap, 0);
                    currentNode = heap[0];
                } 
            }

            while (currentNode[0] != start[0] || currentNode[1]!= start[1]) //determines the backwards path travelled (from end to start)
            {
                tempPreviousCheckNode = grid[currentNode[0], currentNode[1]].PreviousPathNode;
                tempPath.Add(new int[] { currentNode[1] - tempPreviousCheckNode[1],tempPreviousCheckNode[0]- currentNode[0]});
                currentNode = tempPreviousCheckNode;
            }

            previousPathDirection = new int[] { 0, 0 };
            for (int i = tempPath.Count-1;i>=0;i--) //reverses the temporary path and combines scalar multiple directions
            {
                if (i != 0)
                {
                    if ((tempPath[i][0] == 0 && tempPath[i - 1][0] == 0) || (tempPath[i][1] == 0 && tempPath[i - 1][1] == 0)) //if both direction vectors do not move in the x or y direction
                    {
                        previousPathDirection = new int[] { tempPath[i][0] + previousPathDirection[0], tempPath[i][1] + previousPathDirection[1] }; //adds to the storage variable
                        continue;
                    }
                    else if (tempPath[i][0] != 0 && tempPath[i - 1][0] != 0 && tempPath[i][1] != 0 && tempPath[i - 1][1] != 0) //if there are no zeroes (does not allow division)
                    {
                        if ((tempPath[i][0] / tempPath[i - 1][0] == tempPath[i][1] / tempPath[i - 1][1]) && (tempPath[i][0] % tempPath[i - 1][0] == tempPath[i][1] % tempPath[i - 1][1])) //if a scalar multiple of each other
                        {
                            previousPathDirection = new int[] { tempPath[i][0] + previousPathDirection[0], tempPath[i][1] + previousPathDirection[1] }; //adds to the storage variable
                            continue;
                        }
                    }
                }

                path.Add(new int[] { tempPath[i][0] + previousPathDirection[0], tempPath[i][1] + previousPathDirection[1] }); //if not a scalar multiple add the path direction to the storage variable and store that direction vector
                previousPathDirection = new int[] { 0, 0 };
            }
            Console.WriteLine(DateTime.Now - startingTime);
            return path;
        }
        private void RevisitNode(ref Node[,] grid, ref List<int[]> heap, int x, int y, int prevx, int prevy) //adds a node that has already been visited into the heap
        {
            int pos;
            grid[y, x].PreviousPathNode = new int[] { prevy, prevx }; //updates the information for that node
            grid[y, x].DistanceTravelled = grid[grid[y, x].PreviousPathNode[0], grid[y, x].PreviousPathNode[1]].DistanceTravelled + Math.Sqrt(Math.Pow(y - grid[y, x].PreviousPathNode[0], 2) + Math.Pow((x - grid[y, x].PreviousPathNode[1]), 2));
            pos = LinearSearch(ref heap, y, x); //finds the position in the heap if it is in, recieves -1 if it is not in
            if (pos == -1) //if co-ordinate is not in the heap
            {
                heap.Add(new int[] { y, x });
                SortUp(ref grid, ref heap, heap.Count - 1);
            }
            else //is in the heap
            {
                SortUp(ref grid, ref heap, pos);
            }
        }
        private int LinearSearch (ref List<int[]> heap,int y,int x) //finds position of a co-ordinate in the heap, returns -1 if it doesn't exist
        {
            for (int i = 0; i < heap.Count; i++)
            {
                if (heap[i][0] == y && heap[i][1] == x)
                {
                    return i;
                }
            }
            return -1;
        }
        private void HeapSwitch(ref List<int[]> heap, int oldpos, int newpos) //switches the position of two co-ordinates in the heap
        {
            int[] temp;
            temp = heap[oldpos];
            heap[oldpos] = heap[newpos];
            heap[newpos] = temp;
            return;
        }
        private void SortUp(ref Node[,] grid, ref List<int[]> heap, int pos) //sorts a node upwards through a heap
        {
            if (pos == 0)//if at the top of the heap
            {
                return;
            }
            else if (grid[heap[pos][0], heap[pos][1]].Distance < grid[heap[(pos - 1) / 2][0], heap[(pos - 1) / 2][1]].Distance)//if child is less than the root node
            {
                HeapSwitch(ref heap, pos, (pos - 1) / 2);
                SortUp(ref grid, ref heap, (pos - 1) / 2);//gives new position, continues sorting
            }
            return;
        }
        private void SortDown (ref Node[,] grid,ref List<int[]> heap,int pos) //sorts a node down through a heap
        {
            int leastChild;
            if (pos * 2 + 2 > heap.Count) //if at the bottom of the heap
            {
                return;
            }
            else if (pos * 2 + 2 != heap.Count)//if there is a right child node
            {
                leastChild = grid[heap[pos * 2 + 1][0], heap[pos * 2 + 1][1]].Distance < grid[heap[pos * 2 + 2][0], heap[pos * 2 + 2][1]].Distance ? pos * 2 + 1 : pos * 2 + 2;//finds which child node is the least
                if (grid[heap[pos][0], heap[pos][1]].Distance > grid[heap[leastChild][0], heap[leastChild][1]].Distance)//switch if greater than the least child node
                {
                    HeapSwitch(ref heap, pos, leastChild);
                    SortDown(ref grid, ref heap, leastChild);//given new position, continues sorting
                }
                return;
            }
            else if (grid[heap[pos][0], heap[pos][1]].Distance > grid[heap[pos * 2 + 1][0], heap[pos * 2 + 1][1]].Distance)//switch if greater than the left child node
            {
                HeapSwitch(ref heap, pos, pos * 2 + 1);
                SortDown(ref grid, ref heap, pos * 2 + 2);//given new position, continues sorting
            }
            return; //occurs if root is now/was greater than nodes
        }
        private bool AddToHeap(ref Node[,] grid, int x, int y, int [] end,bool firstAdded,ref List<int[]> heap,int oldy, int oldx) //adds a node to the heap
        {
            grid[y, x].PreviousPathNode = grid[oldy, oldx].IsCorner == true ? new int[] { oldy, oldx } : grid[oldy, oldx].PreviousPathNode; //sets information for node
            grid[y, x].Heuristic = Math.Sqrt(Math.Pow(x - end[1], 2) + Math.Pow(y - end[0], 2));
            grid[y, x].DistanceTravelled = grid[grid[y, x].PreviousPathNode[0], grid[y, x].PreviousPathNode[1]].DistanceTravelled + Math.Sqrt(Math.Pow(y - grid[y, x].PreviousPathNode[0], 2) + Math.Pow((x - grid[y, x].PreviousPathNode[1]), 2));
            
            if (firstAdded == true) //if it's the first being added from the current node, it replaces the current node in the heap and is sorted down
            {
                heap[0] = new int[] { y, x };
                SortDown(ref grid, ref heap, 0);
            }
            else //if it's not the first node, it's added to the end of the heap and sorts upwards through the heap
            {
                heap.Add(new int[] { y, x });
                SortUp(ref grid, ref heap, heap.Count - 1);
            }
            return false;
        }
        private Node[,] MakeArray(char[,] cameraGrid) //creates the basic node array
        {
            int height=cameraGrid.GetLength(0),width =cameraGrid.GetLength(1) ;
            Node [,] grid = new Node [height,width];
            for (int i = 0; i < height; i++) //traverses through all the positions in the array
            {
                for (int j = 0; j < width; j++)
                {
                    grid[i, j].AreaType = cameraGrid[i, j]; //sets the type of the node
                    grid[i, j].DistanceTravelled = -1; //sets the distance travelled to -1, the default, which means that it hasn't been visited
                }
            }
            return grid;
        }
        private void FindLocation(char[,] cameraGrid, ref int[] start, ref int[] end) //finds the location of start and end if not already set
        {
            int num;
            char[] check = new char[2];//check holds what needs to be searched for
            int s = start[0] + start[1], e = end[0] + end[1];//determines if the positions are -1, which means they have not been set
            if ((s<=-2)||(e<=-2))//if either start or end does not have a value
            {
                if ((s <= -2) && (e <= -2))//if both don't
                {
                    check = new char[2] { 'e', 's' };
                    num = 2;
                }
                else//if only one doesn't
                {
                    num = 1;
                    if (s <= -2)//if s doesn't have a position
                    {
                        check = new char[1] { 's' };
                    }
                    if (s <= -2)//if e doesn't have a position
                    {
                        check = new char[1] { 'e' };
                    }
                }
                for (int i1 = 0; i1 < cameraGrid.GetLength(0) && num > 0; i1++)//runs through height of cameraGrid
                {
                    for (int i2 = 0; i2 < cameraGrid.GetLength(1) && num > 0; i2++)//runs through width of cameraGrid
                    {
                        for (int i3 = 0; i3 < num; i3++)//runs through what needs to be checked
                        {
                            if (check[i3] == cameraGrid[i1, i2])//if it's the value being looked for
                            {
                                if (check[i3]=='s')//will reduce the num, so that it doesn't check for s anymore
                                {
                                    start = new int []{i1,i2};
                                    num = 1;
                                    break;
                                }
                                else//will reduce the num and switches s to the front, so that it doesn't search for e anymore
                                {
                                    end=new int[]{i1,i2};
                                    num = 1;
                                    check[0] = 's';
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}