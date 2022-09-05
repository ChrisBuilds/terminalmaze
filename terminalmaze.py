#!/usr/bin/python3

from maze_algorithms.huntandkill import HuntandKill
from maze_algorithms.wilsons import Wilsons
from maze_algorithms.binarytree import BinaryTree
from maze_algorithms.sidewinder import Sidewinder
from maze_algorithms.aldousbroder import AldousBroder
from maze_algorithms.recursivebacktracker import RecursiveBacktracker
from solve_algorithms.breadthfirst import BreadthFirst
from grid.grid import Grid

from time import sleep
import sys


def main():
    mask = """
##  ############################################################
##                                                            ##  
##  ########  ##    ## ######## ##     ##  #######  ##    ##  ##
##  ##     ##  ##  ##     ##    ##     ##        ## ###   ##  ##
##              ####      ##    ##     ## ##     ## ####  ##  ##
##  ########     ##       ##    ######### ##     ## ## ## ##  ##
##  ##           ##       ##    ##     ## ##     ## ##  ####  ##
##  ##           ##       ##    ##     ## ##        ##   ###  ##
##  ##           ##       ##    ##     ##  #######  ##    ##  ##
##                                                            ##
############################################################  ##
    """
    mask = """
    ######  ########     ###     ######  ########          
   ##    ##        ##   ## ##   ##    ## ##                
   ##       ##                  ##       ##                
    ######  ########  ##     ## ##       ######            
         ## ##        ######### ##       ##                
   ##    ## ##        ##     ## ##    ## ##                
    ######  ##        ##     ##  ######  ########
          
   ###    ##     ##    ###    ##    ## ########     ###    
  ## ##   ###   ###   ## ##   ###   ##        ##   ## ##   
          #### ####           ####  ## ##     ##           
##     ## ## ### ## ##     ## ## ## ## ##     ## ##     ## 
######### ##     ## ######### ##  #### ##     ## ######### 
##     ## ##     ## ##     ## ##   ### ##        ##     ## 
##     ## ##     ## ##     ## ##    ## ########  ##     ## 
    """

    showlogic = True
    maze = Grid(100, 27, mask=mask)
    # algo = BinaryTree(maze, showlogic=showlogic)
    # algo = Sidewinder(maze, showlogic=showlogic)
    # algo = AldousBroder(maze, showlogic=showlogic)
    # algo = Wilsons(maze, showlogic=showlogic)
    # algo = HuntandKill(maze, showlogic=showlogic)
    algo = RecursiveBacktracker(maze, showlogic=showlogic)
    solver = BreadthFirst(maze)
    try:
        maze: Grid
        for maze in algo.generate_maze():
            maze.visual.show(algo.logic_data, showlogic)
            sleep(0.0125)
        for maze in solver.solve():
            maze.visual.show(solver.logic_data, showlogic)
            sleep(0.0125)
    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


if __name__ == "__main__":
    main()
