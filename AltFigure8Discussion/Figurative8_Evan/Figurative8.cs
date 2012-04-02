/**
 * This is the brainstorming code I wrote earlier for the alternate implementation of Figure 8 where gates are opened and closed as the robot proceeds.
 * Since the current code reportedly works well at finding holes from Andy's image recognition, I'm not sure this approach will be necessary.
 * Regardless, it's a possible alternative if testing brings up any problems that can't be otherwise corrected.
 * 
 * Crude demonstration of a potential strategy for processing an input image recognition source and isolating gate locations.
 *
 * After the processing has finished, the gates can be opened and closed individually as the robot navigates the course
 * and a simple pathing command to any point on the opposite side of a wall will allow Astar to navigate any gap in the wall.
 * 
 * IsRobotLeftOfLeftWall?
 * OpenGate1.
 * GoToTheMiddle.
 * IsRobotInTheMiddle?
 * CloseGate1.
 * OpenGate2.
 * GoToTheRight.
 * IsRobotToTheRight?
 * CloseGate2.
 * OpenGate3.
 * GoToTheMiddle... etc.
 * 
 * No data is lost during processing.  The 'Z' flag is used to denote an empty space that should appear blocked to Astar for the purpose of pathing through the correct gate.
 * They should mostly appear along parts of the wall that appeared as free space, but are not actually full gaps through the wall.
 * In the event that the robot finds somehow finds itself in a bizarre location with no way to get to its destination, then these
 * blocks can still be differentiated from their more unforgiving 'X' brethren.
 * 
 * Currently makes a number of assumptions.  Important ones to address include:
 * The location of gates relative to one another on the wall, currently assumed to be one gate in top half and one gate in bottom half.
 * No, (or minimal) "bubbles" (hollow sections surrounded by barriers) forming in the walls.
 * Currently uses densest concentration of barrier blocks to isolate walls.  This could be replaced with an algorithm that looks for the narrowest gap that must be traversed.
 * 30x30 grid is utilized
 * 
 * IMPORTANT EDIT: If the current hole-finding algorithm is already very resistant to errors, then this discussion is pretty much irrelevant.
 * However, we would require a method of converting the current implementation for finding critical points on either side of the wall into finding
 * holes in the wall themselves.
 * 
 * The most important issue to keep in mind in this implementation is the possibility that the left wall may be located off-center, especially
 * in the event of "bubbles" in the middle of the wall.  This could cause the largest gap in the section of wall analyzed to not accurately line
 * up to the gate, and thus create an impassable barrier.  Thankfully a few simple safety checks should be able to make sure this doesn't happen.
 * One possible simple implementation a basic check would be to simply check to ensure free space on either side of any potential "gap square" before
 * considering it a proper gap.
 * 
 * Example of failing section of wall, where the left edge is considered the densest section:
 * 
 * XXX                  XXX
 * XXX                  XXX
 *                      X  
 * X X                  X X
 *  X       processed   1X
 *  X        ------->   1X
 *  X                   1X
 *  XX                  1XX
 * X X                  X X
 * X X                  X X
 * X                    X
 * 
 * 
 * WARNING: Complete lack of regard for the principles of encapsulation and OOP to follow. :)  I'll rewrite a *much* more polished
 * implementation if we decide to go for this approach.
 */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Figurative8_Evan
{
    class Figure8Test
    {
        int leftwallindex;
        int rightwallindex;

        int[] gate1index, gate2index, gate3index, gate4index; //should be a 2d array ideally
        char[,] board;
        public Figure8Test()
        {
            //30x30 test grid
            board = new char[,] { {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', 'X', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', 'X', 'X', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', '-', '-','-','-','-'},
                                    {'-', '-', '-', '-', 'X', 'X', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'X', 'X', 'X', 'X', 'X', '-','-','-','-'}};

            char[,] testprocessed = processField(ref board);

            for (int i = 0; i < 30; ++i)
            {
                for (int j = 0; j < 30; ++j)
                {
                    System.Console.Write(board[i, j] + " ");
                }
                System.Console.WriteLine();
            }
            System.Console.WriteLine();
            System.Console.WriteLine();
            System.Console.WriteLine();
            for (int i = 0; i < 30; ++i)
            {
                for (int j = 0; j < 30; ++j)
                {
                    System.Console.Write(testprocessed[i, j] + " ");
                }
                System.Console.WriteLine();
            }

            System.Console.ReadLine();
        }

        //Isolates gate indicies, adds walls to block off all non-gate squares.
        char[,] processField(ref char[,] f)
        {
            //I fairly confident Nx and Ny are used backwards at several points during this example.
            int Nx = 30;
            int Ny = 30;

            char[,] modified = new char[Nx, Ny];

            //copies f into modified.  later combine processing steps together.
            for (int i = 0; i < Nx; i++)
            {
                for (int j = 0; j < Ny; j++)
                {
                    modified[i, j] = f[i, j];
                }
            }

            int blockcount = 0, maxblockcount = 0;
            int maxloc = -1;

            //finds the location of the wall on the horizontal axis. TODO: Eventually combine loops together.
            for (int i = 0; i < Nx/2; i++) //search first half of the board for the first wall
            {
                for (int j = 0; j < Ny; j++)
                {
                    if (modified[j, i] == 'X')
                        blockcount++;
                }

                if (blockcount > maxblockcount)
                {
                    maxblockcount = blockcount;
                    maxloc = i;
                }

                blockcount = 0;
            }

            if (maxloc <= 0)
            {
                System.Console.WriteLine("Error, no valid left wall found.");//exceptions etc
            }
            else
                leftwallindex = maxloc;

            maxloc = -1;
            maxblockcount = 0;
            blockcount = 0;

            for (int i = Nx/2; i < Nx; i++)
            {
                for (int j = 0; j < Ny; j++)
                {
                    if (modified[j, i] == 'X')
                        blockcount++;
                }

                if (blockcount > maxblockcount)
                {
                    maxblockcount = blockcount;
                    maxloc = i;
                }

                blockcount = 0;
            }

            if (maxloc <= 0)
            {
                System.Console.WriteLine("Error, no valid right wall found.");//exceptions etc
            }
            else
                rightwallindex = maxloc;


            System.Console.WriteLine("Right wall at: " + rightwallindex);
            System.Console.WriteLine("Left wall at: " + leftwallindex);

            //search the top half of the left wall for the first gap
            int gapcount = 0, gapmax = 0;
            int gaptoploc = -1;
            int maxgaptoploc = -1;
            bool firstflag = true;

            for (int j = 0; j < Ny/2; j++)
            {
                if (modified[j, leftwallindex] == '-')
                {
                    if (firstflag){
                        gaptoploc = j;
                        firstflag = false;
                    }

                    gapcount++;
                }
                else
                {
                    firstflag = true;
                    if (gapcount > gapmax)
                    {
                        gapmax = gapcount;
                        maxgaptoploc = gaptoploc;
                    }

                    gapcount = 0;
                 }
            }

            for (int i = maxgaptoploc; i < gapmax + maxgaptoploc; ++i)
            {
                modified[i, leftwallindex] = '1';
            }

            //search the bottom half of the left wall for the fourth gate
            gapcount = 0;
            gapmax = 0;
            gaptoploc = -1;
            maxgaptoploc = -1;
            firstflag = true;

            for (int j = Ny/2; j < Ny; j++)
            {
                if (modified[j, leftwallindex] == '-')
                {
                    if (firstflag){
                        gaptoploc = j;
                        firstflag = false;
                    }

                    gapcount++;
                }
                else
                {
                    firstflag = true;
                    if (gapcount > gapmax)
                    {
                        gapmax = gapcount;
                        maxgaptoploc = gaptoploc;
                    }
                    gapcount = 0;
                 }
            }

            for (int i = maxgaptoploc; i < gapmax + maxgaptoploc; ++i)
            {
                modified[i, leftwallindex] = '4';
            }

            //search the top half of the right wall for the third gap
            gapcount = 0;
            gapmax = 0;
            gaptoploc = -1;
            maxgaptoploc = -1;
            firstflag = true;

            for (int j = 0; j < Ny/2; j++)
            {
                if (modified[j, rightwallindex] == '-')
                {
                    if (firstflag)
                    {
                        gaptoploc = j;
                        firstflag = false;
                    }

                    gapcount++;
                }
                else
                {
                    firstflag = true;
                    
                    if (gapcount > gapmax)
                    {
                        gapmax = gapcount;
                        maxgaptoploc = gaptoploc;
                    }
                    gapcount = 0;
                }
            }

            for (int i = maxgaptoploc; i < gapmax+maxgaptoploc; ++i)
            {
                modified[i, rightwallindex] = '3';
            }

            //search the bottom half of the right wall for the second gate
            gapcount = 0;
            gapmax = 0;
            gaptoploc = -1;
            maxgaptoploc = -1;
            firstflag = true;

            for (int j = Ny / 2; j < Ny; ++j)
            {
                if (modified[j, rightwallindex] == '-')
                {
                    if (firstflag)
                    {
                        gaptoploc = j;
                        firstflag = false;
                    }

                    gapcount++;
                }
                else
                {
                    firstflag = true;
                    
                    if (gapcount > gapmax)
                    {
                        gapmax = gapcount;
                        maxgaptoploc = gaptoploc;
                    }
                    gapcount = 0;
                }
            }

            for (int i = maxgaptoploc; i < gapmax + maxgaptoploc; ++i)
            {
                modified[i, rightwallindex] = '2';
            }

            //Modify the board to make sure that the gates are the only possible routes.
            for (int i = 0; i < Ny; ++i)
            {
                if (modified[i, leftwallindex] == '-')
                    modified[i, leftwallindex] = 'Z'; //Z flag should be treated as "blocked" by Astar.
                if (modified[i, rightwallindex] == '-')
                    modified[i, rightwallindex] = 'Z';
            }

            return modified;
        }
    }
}
