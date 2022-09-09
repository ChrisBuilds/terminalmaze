#!/usr/bin/python3

from terminalmaze.algorithms.gen.huntandkill import HuntandKill
from terminalmaze.algorithms.gen.wilsons import Wilsons
from terminalmaze.algorithms.gen.binarytree import BinaryTree
from terminalmaze.algorithms.gen.sidewinder import Sidewinder
from terminalmaze.algorithms.gen.aldousbroder import AldousBroder
from terminalmaze.algorithms.gen.recursivebacktracker import RecursiveBacktracker
from terminalmaze.algorithms.gen.primssimple import PrimsSimple
from terminalmaze.algorithms.gen.primsweighted import PrimsWeighted
from terminalmaze.algorithms.gen.kruskalsrandomized import KruskalsRandomized
from terminalmaze.algorithms.gen.ellers import Ellers
from terminalmaze.algorithms.solve.breadthfirst import BreadthFirst
from terminalmaze.resources.grid import Grid

from time import sleep
import sys
import random


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
    maze = Grid(105, 27, mask_string=amanda_inv)
    seed = int().from_bytes(random.randbytes(5), byteorder="big")
    maze.seed = seed
    # algo = BinaryTree(maze, showlogic=show_mazelogic)
    # algo = Sidewinder(maze, showlogic=show_mazelogic)
    # algo = AldousBroder(maze, showlogic=show_mazelogic)
    # algo = Wilsons(maze, showlogic=show_mazelogic)
    # algo = HuntandKill(maze, showlogic=show_mazelogic)
    algo = RecursiveBacktracker(maze, showlogic=show_mazelogic)
    # algo = PrimsSimple(maze, showlogic=show_mazelogic)
    # algo = PrimsWeighted(maze, showlogic=show_mazelogic)
    # algo = KruskalsRandomized(maze, showlogic=show_mazelogic)
    # algo = Ellers(maze, showlogic=show_mazelogic)
    solver = BreadthFirst(maze, showlogic=show_solvelogic)
    try:
        maze: Grid
        for maze in algo.generate_maze():
            maze.visual.show(algo.visual_effects, algo.status_text, show_mazelogic)
            sleep(0.0135)
        for maze in solver.solve():
            maze.visual.show(solver.visual_effects, solver.status_text, show_solvelogic)
            sleep(0.0135)
    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


if __name__ == "__main__":
    main()
