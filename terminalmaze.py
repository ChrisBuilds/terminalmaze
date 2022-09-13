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
from terminalmaze.config import tm_config, tm_masks

from time import sleep
import sys
import random


def get_mask() -> str | None:
    """
    Check the masks directory for the configured mask and return the mask as a string.
    Returns
    -------
    str | None : mask string if found, else None
    """
    if tm_config["global"]["mask"] in tm_masks:
        with open(tm_masks[tm_config["global"]["mask"]], "r") as mask_file:
            mask = mask_file.read()
    else:
        mask = None
    return mask


def main():
    solve = tm_config["global"]["run_solver"]
    maze = Grid(105, 27, mask_string=get_mask())
    seed = int().from_bytes(random.randbytes(5), byteorder="big")
    maze.seed = seed
    # algo = BinaryTree(maze)
    # algo = Sidewinder(maze)
    # algo = AldousBroder(maze)
    # algo = Wilsons(maze)
    # algo = HuntandKill(maze)
    algo = RecursiveBacktracker(maze)
    # algo = PrimsSimple(maze)
    # algo = PrimsWeighted(maze)
    # algo = KruskalsRandomized(maze)
    # algo = Ellers(maze)
    solver = BreadthFirst(maze)
    try:
        maze: Grid
        for maze in algo.generate_maze():
            maze.visual.show(algo.visual_effects, algo.status_text, subject="maze")
        else:
            maze.visual.show(algo.visual_effects, algo.status_text, subject="maze", complete=True)
            print()
        if solve:
            for maze in solver.solve():
                maze.visual.show(solver.visual_effects, solver.status_text, subject="solve")
            else:
                maze.visual.show(solver.visual_effects, solver.status_text, subject="solve", complete=True)
                print()
    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


if __name__ == "__main__":
    main()
