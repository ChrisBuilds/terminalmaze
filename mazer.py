#!/usr/bin/python3

from aldousbroder import AldousBroder
from binary_tree import BinaryTree
from sidewinder import Sidewinder
from aldousbroder import AldousBroder
from huntandkill import HuntandKill
from wilsons import Wilsons
from recursivebacktracker import RecursiveBacktracker
from grid import Grid


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

    grid = Grid(20, 10, mask=gen_mask(mask))
    # maze = BinaryTree(grid)
    # maze = Sidewinder(grid)
    # maze = AldousBroder(grid)
    # maze = Wilsons(grid)
    # maze = HuntandKill(grid)
    maze = RecursiveBacktracker(grid)


if __name__ == "__main__":
    main()
