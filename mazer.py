#!/usr/bin/python3

from aldousbroder import AldousBroder
from binary_tree import BinaryTree
from sidewinder import Sidewinder
from aldousbroder import AldousBroder
from huntandkill import HuntandKill
from wilsons import Wilsons
from recursivebacktracker import RecursiveBacktracker
from grid import Grid
from terminal_grid import TermGrid
import curses, time


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

    grid = Grid(50, 20, mask=gen_mask(mask))
    # maze = BinaryTree(grid, screen)
    # maze = Sidewinder(grid, screen)
    # maze = AldousBroder(grid, screen)
    # maze = Wilsons(grid, screen)
    # maze = HuntandKill(grid, screen)
    maze = RecursiveBacktracker(grid)
    time.sleep(5)


if __name__ == "__main__":
    main()
