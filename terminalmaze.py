#!/usr/bin/python3

from maze_algorithms.huntandkill import HuntandKill
from maze_algorithms.wilsons import Wilsons
from maze_algorithms.binarytree import BinaryTree
from maze_algorithms.sidewinder import Sidewinder
from maze_algorithms.aldousbroder import AldousBroder
from maze_algorithms.recursivebacktracker import RecursiveBacktracker
from maze_algorithms.primssimple import PrimsSimple
from maze_algorithms.primsweighted import PrimsWeighted
from solve_algorithms.breadthfirst import BreadthFirst
from grid.grid import Grid

from time import sleep
import sys


def main():
    python = """
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
    amanda_inv = """
m:    ######  ########     ###     ######  #########
m:  ##      ##        #####   #####      ##        #
m:  #  ####  #  #####  ###  #  ###  ####  #  #######
m:  #  #######  #####  ##  ###  ##  #######  ####
m:  ##      ##        ##  #####  #  #######     #
m:  #######  #  ########         #  #######  ####
m:  #  ####  #  ########  #####  #  ####  #  #######
m:  ##      ##  ########  #####  ##      ##        #
m:    # ####   #        #      ##   ### ##  ### ####
m:
m:    # #    #      ##    # #    ##     # ##### ##     ## 
m:   #   ####  #####  ####   ####  ####  #        #####   #
m:  #  #  ###   ###   ###  #  ###   ###  #  #####  ###  #  #
m: #  ###  ##    #    ##  ###  ##    ##  #  #####  ##  ###  #
m:#  #####  #  #   #  #  #####  #  #  #  #  #####  #  #####  #
m:#         #  #####  #         #  ##    #  #####  #         #
m:#  #####  #  #####  #  #####  #  ###   #  #####  #  #####  #
m:#  #####  #  #####  #  #####  #  ####  #        ##  #####  #
m: ##     ## ##     ## ##     ## ##    ## ########  ##     ##
    """
    amanda = """
m:    ######  ########     ###     ######  ########          
m:   ##    ##        ##   ## ##   ##    ## ##                
m:   ##       ##                  ##       ##                
m:    ######  ########  ##     ## ##       ######            
m:         ## ##        ######### ##       ##                
m:   ##    ## ##        ##     ## ##    ## ##                
m:    ######  ##        ##     ##  ######  ########
m:
m:   ###    ##     ##    ###    ##    ## ########     ###    
m:  ## ##   ###   ###   ## ##   ###   ##        ##   ## ##   
m:          #### ####           ####  ## ##     ##           
m:##     ## ## ### ## ##     ## ## ## ## ##     ## ##     ## 
m:######### ##     ## ######### ##  #### ##     ## ######### 
m:##     ## ##     ## ##     ## ##   ### ##        ##     ## 
m:##     ## ##     ## ##     ## ##    ## ########  ##     ##     
    """

    show_mazelogic = True
    show_solvelogic = True
    maze = Grid(105, 27, mask=amanda_inv)
    # algo = BinaryTree(maze, showlogic=show_mazelogic)
    # algo = Sidewinder(maze, showlogic=show_mazelogic)
    # algo = AldousBroder(maze, showlogic=show_mazelogic)
    # algo = Wilsons(maze, showlogic=show_mazelogic)
    # algo = HuntandKill(maze, showlogic=show_mazelogic)
    # algo = RecursiveBacktracker(maze, showlogic=show_mazelogic)
    # algo = PrimsSimple(maze, showlogic=show_mazelogic)
    algo = PrimsWeighted(maze, showlogic=show_mazelogic)
    solver = BreadthFirst(maze, showlogic=show_solvelogic)
    try:
        maze: Grid
        for maze in algo.generate_maze():
            maze.visual.show(algo.logic_data, algo.status_text, show_mazelogic)
            sleep(0.0135)
        for maze in solver.solve():
            maze.visual.show(solver.logic_data, solver.status_text, show_solvelogic)
            sleep(0.0135)
    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


if __name__ == "__main__":
    main()
