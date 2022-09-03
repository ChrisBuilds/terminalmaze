#!/usr/bin/python3

from maze_algorithms.huntandkill import HuntandKill
from maze_algorithms.wilsons import Wilsons
from maze_algorithms.binarytree import BinaryTree
from maze_algorithms.sidewinder import Sidewinder
from maze_algorithms.aldousbroder import AldousBroder
from maze_algorithms.recursivebacktracker import RecursiveBacktracker
from grid.grid import Grid
import colored
from time import sleep
from os import system
import sys


def gen_mask(mask):
    mask = [line.strip() for line in mask.split("\n") if line.strip()]
    return mask


def main():
    mask = """
    ..........
    ..........
    ....xxx...
    ....xxx...
    ....xxx...
    ..........
    ..........
    ..........
    ..........
    ..........
    """
    showlogic = True
    mazegrid = Grid(30, 15, mask=gen_mask(mask))
    algo = BinaryTree(mazegrid, showlogic=showlogic)
    # algo = Sidewinder(mazegrid, showlogic=showlogic)
    # algo = AldousBroder(mazegrid, showlogic=showlogic)
    # algo = Wilsons(mazegrid, showlogic=showlogic)
    # algo = HuntandKill(mazegrid, showlogic=showlogic)
    # algo = RecursiveBacktracker(mazegrid, showlogic=showlogic)
    try:
        for maze in algo.generate_maze():
            show_maze(maze, algo.logic_data, showlogic)
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
        "logic0": colored.fg(237),
        "logic1": colored.fg(28),
    }
    working_cell = logic_data.get("working_cell")
    last_linked = logic_data.get("last_linked")
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
    sleep(0.05)


if __name__ == "__main__":
    main()
