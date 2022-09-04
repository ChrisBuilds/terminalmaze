#!/usr/bin/python3

from maze_algorithms.huntandkill import HuntandKill
from maze_algorithms.wilsons import Wilsons
from maze_algorithms.binarytree import BinaryTree
from maze_algorithms.sidewinder import Sidewinder
from maze_algorithms.aldousbroder import AldousBroder
from maze_algorithms.recursivebacktracker import RecursiveBacktracker
from solve_algorithms.breadthfirst import BreadthFirst
from grid.grid import Grid

import colored
from time import sleep
from os import system
import sys


def gen_mask(mask):
    mask = [line.strip("\n") for line in mask.split("\n") if "#" in line]
    return mask


def main():
    mask = """
########  ##    ## ######## ##     ##  #######  ##    ## 
##     ##  ##  ##     ##    ##     ##        ## ###   ## 
            ####      ##    ##     ## ##     ## ####  ## 
########     ##       ##    ######### ##     ## ## ## ## 
##           ##       ##    ##     ## ##     ## ##  #### 
##           ##       ##    ##     ## ##        ##   ### 
##           ##       ##    ##     ##  #######  ##    ## 
    """
    #    mask = """
    ###
    ###
    ###
    # """
    showlogic = True
    maze = Grid(80, 20, mask=gen_mask(mask))
    algo = BinaryTree(maze, showlogic=showlogic)
    # algo = Sidewinder(maze, showlogic=showlogic)
    # algo = AldousBroder(maze, showlogic=showlogic)
    # algo = Wilsons(maze, showlogic=showlogic)
    # algo = HuntandKill(maze, showlogic=showlogic)
    # algo = RecursiveBacktracker(maze, showlogic=showlogic)

    solver = BreadthFirst(maze)
    try:
        for maze in algo.generate_maze():
            show_maze(maze, algo.logic_data, showlogic)
        for maze in solver.solve():
            show_maze(maze, solver.logic_data, True)
    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


def add_logic_data(visual_grid, logic_data):
    def translate_cell_coords(cell):
        row = cell.row
        column = cell.column
        if row == 0:
            row = 1
        else:
            row = (row * 2) + 1
        if column == 0:
            column = 1
        else:
            column = (column * 2) + 1
        return row, column

    def update_visual_grid(cell, color):
        y, x = translate_cell_coords(cell)
        visual_grid[y][x] = f"{color}{chr(9608)}"

    color_map = {
        "working_cell": colored.fg(14),
        "last_linked": colored.fg(2),
        "invalid_neighbors": colored.fg(52),
        "frontier": colored.fg(72),
        "explored": colored.fg(137),
        "position": colored.fg(76),
        "target": colored.fg(202),
        "start": colored.fg(211),
        "path": colored.fg(133),
        "logic0": colored.fg(237),
        "logic1": colored.fg(28),
    }
    for label, data in logic_data.items():
        if isinstance(data, list):
            for cell in data:
                update_visual_grid(cell, color_map[label])
        else:
            update_visual_grid(data, color_map[label])

    return visual_grid


def show_maze(maze, logic_data, showlogic):
    visual_grid = maze.get_visual_grid()
    if showlogic:
        visual_grid = add_logic_data(visual_grid, logic_data)
    lines = ["".join(line) for line in visual_grid]
    system("clear")
    print("\n".join(lines))
    sleep(0.03)


if __name__ == "__main__":
    main()
