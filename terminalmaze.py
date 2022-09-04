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
    mask = [line.strip("\n") for line in mask.split("\n")]
    return mask


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
    #    mask = """
    ###
    ###
    ###
    # """
    showlogic = True
    maze = Grid(20, 10, mask=None)
    # algo = BinaryTree(maze, showlogic=showlogic)
    # algo = Sidewinder(maze, showlogic=showlogic)
    # algo = AldousBroder(maze, showlogic=showlogic)
    # algo = Wilsons(maze, showlogic=showlogic)
    # algo = HuntandKill(maze, showlogic=showlogic)
    algo = RecursiveBacktracker(maze, showlogic=showlogic)
    solver = BreadthFirst(maze)
    try:
        for maze in algo.generate_maze():
            show_maze(maze, algo.logic_data, showlogic)
        for maze in solver.solve():
            show_maze(maze, solver.logic_data, True)
    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


def add_logic_data(visual_grid, logic_data, maze: Grid):
    def update_visual_grid(visual_coordinates, color):
        y, x = visual_coordinates
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
            translated_cells = set(maze.translate_cell_coords(cell) for cell in data)
            for visual_coordinates in maze.visual_links:
                visual_y, visual_x = visual_coordinates
                if (
                    (visual_y + 1, visual_x) in translated_cells
                    and (visual_y - 1, visual_x) in translated_cells
                ) or (
                    (visual_y, visual_x + 1) in translated_cells
                    and (visual_y, visual_x - 1) in translated_cells
                ):
                    translated_cells.add(visual_coordinates)
            for visual_coordinates in translated_cells:
                update_visual_grid(visual_coordinates, color_map[label])
        else:
            visual_coordinates = maze.translate_cell_coords(data)
            update_visual_grid(visual_coordinates, color_map[label])

    return visual_grid


def show_maze(maze: Grid, logic_data, showlogic):
    visual_grid = [l.copy() for l in maze.visual_grid]
    if showlogic:
        visual_grid = add_logic_data(visual_grid, logic_data, maze)
    lines = ["".join(line) for line in visual_grid]
    system("clear")
    print("\n".join(lines))
    # sleep(0.0125)


if __name__ == "__main__":
    main()
