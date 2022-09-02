#!/usr/bin/python3

from audioop import add
from aldousbroder import AldousBroder
from binary_tree import BinaryTree
from sidewinder import Sidewinder
from aldousbroder import AldousBroder
from huntandkill import HuntandKill
from wilsons import Wilsons
from recursivebacktracker import RecursiveBacktracker
from grid import Grid
from os import system
import colorama
from time import sleep


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
    grid = Grid(40, 20, mask=gen_mask(mask))
    # maze = BinaryTree(grid)
    # maze = Sidewinder(grid)
    # maze = AldousBroder(grid)
    # maze = Wilsons(grid)
    # maze = HuntandKill(grid)
    algo = RecursiveBacktracker(grid, showlogic=showlogic)

    for maze in algo.generate_maze():
        show_maze(maze, algo.logic_data, showlogic)


def add_logic_data(visual_grid, logic_data):
    def translate_cell_coords(cell):
        y = cell.row
        x = cell.column
        if y == 0:
            y = 1
        else:
            y = (y * 2) + 1
        if x == 0:
            x = 1
        else:
            x = (x * 2) + 1
        return (y, x)

    working_cell = logic_data["working_cell"]
    last_linked = logic_data["last_linked"]
    # color working cell
    y, x = translate_cell_coords(working_cell)
    visual_grid[y][x] = f"{colorama.Fore.CYAN}{chr(9608)}{colorama.Fore.RESET}"
    # color last linked cell
    if last_linked:
        y, x = translate_cell_coords(last_linked)
        visual_grid[y][x] = f"{colorama.Fore.LIGHTYELLOW_EX}{chr(9608)}{colorama.Fore.RESET}"
    return visual_grid


def show_maze(maze, logic_data, showlogic):
    visual_grid = maze.get_visual_grid()
    if showlogic:
        if logic_data["working_cell"]:
            visual_grid = add_logic_data(visual_grid, logic_data)
    lines = ["".join(line) for line in visual_grid]
    system("clear")
    print("\n".join(lines))
    # sleep(0.05)


if __name__ == "__main__":
    main()
