#!/usr/bin/python3

from maze_algorithms.huntandkill import HuntandKill
from maze_algorithms.wilsons import Wilsons
from maze_algorithms.binarytree import BinaryTree
from maze_algorithms.sidewinder import Sidewinder
from maze_algorithms.aldousbroder import AldousBroder
from maze_algorithms.recursivebacktracker import RecursiveBacktracker
from grid.grid import Grid
import colorama
from time import sleep
from os import system


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
    colorama.init()
    showlogic = True
    mazegrid = Grid(40, 20, mask=gen_mask(mask))
    # maze = BinaryTree(grid)
    # maze = Sidewinder(grid)
    # maze = AldousBroder(grid)
    # maze = Wilsons(grid)
    algo = HuntandKill(mazegrid)
    # algo = RecursiveBacktracker(grid, showlogic=showlogic)

    for maze in algo.generate_maze():
        show_maze(maze, algo.logic_data, showlogic)


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

    working_cell = logic_data["working_cell"]
    last_linked = logic_data["last_linked"]
    # color working cell
    y, x = translate_cell_coords(working_cell)
    visual_grid[y][x] = f"{colorama.Fore.CYAN}{chr(9608)}{colorama.Fore.RESET}"
    # color last linked cell
    if last_linked:
        y, x = translate_cell_coords(last_linked)
        visual_grid[y][
            x
        ] = f"{colorama.Fore.LIGHTYELLOW_EX}{chr(9608)}{colorama.Fore.RESET}"
    return visual_grid


def show_maze(maze, logic_data, showlogic):
    visual_grid = maze.get_visual_grid()
    if showlogic:
        if logic_data.get("working_cell"):
            visual_grid = add_logic_data(visual_grid, logic_data)
    lines = ["".join(line) for line in visual_grid]
    system("clear")
    print("\n".join(lines))
    sleep(0.05)


if __name__ == "__main__":
    main()
