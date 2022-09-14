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
from terminalmaze.config import tm_config, tm_masks, tm_themes
import sys
import random
import argparse


MAZE_ALGORITHMS = {
    "binary_tree": BinaryTree,
    "sidewinder": Sidewinder,
    "aldous_broder": AldousBroder,
    "wilsons": Wilsons,
    "hunt_and_kill": HuntandKill,
    "recursive_backtracker": RecursiveBacktracker,
    "prims_simple": PrimsSimple,
    "prims_weighted": PrimsWeighted,
    "kruskals_randomized": KruskalsRandomized,
    "ellers": Ellers,
}

SOLVE_ALGORITHMS = {"breadth_first": BreadthFirst}


def parse_args() -> argparse.ArgumentParser:
    """
    Parse the arguments passed to at the command line.
    Returns
    -------
    args (argparse.ArgumentParser) : arguments parsed
    """
    parser = argparse.ArgumentParser(description="Generate and solve mazes in the terminal")
    parser.add_argument(
        "height",
        metavar="HEIGHT",
        type=int,
        help="int > 0: height of the maze grid in lines, multiply desired height by 2 (each cell has a wall)",
    )
    parser.add_argument(
        "width",
        metavar="WIDTH",
        type=int,
        help="int > 0: width of the maze grid in characters, multiply desired width by 2 (each cell has a wall",
    )
    parser.add_argument(
        "maze_algorithm",
        metavar="MAZE_ALGORITHM",
        type=str,
        help=f"The maze algorithm used for maze generation. Use -ma with no parameters for a list of supported "
        f"algorithms",
        choices=list(MAZE_ALGORITHMS.keys()),
    )
    parser.add_argument(
        "-sa",
        "--solve_algorithm",
        metavar="ALGORITHM",
        type=str,
        help="The solve algorithm used to solve the maze. Use -ma with no parameters for a list of supported "
        f"algorithms",
        required=False,
        default=None,
        choices=list(SOLVE_ALGORITHMS.keys()),
    )
    parser.add_argument(
        "-t",
        "--theme",
        metavar="THEME",
        type=str,
        help="Name of a theme in the themes folder, without the file extension .toml",
        required=False,
        default="default",
    )
    parser.add_argument(
        "-s",
        "--seed",
        metavar="SEED",
        type=int,
        help="Seed to pass to random generator, use to reproduce mazes",
        required=False,
        default=None,
    )
    args = parser.parse_args()
    return args


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


def get_theme(args) -> dict[str, dict[str, int | list[int]]]:
    """
    Get the theme specified in the config file from the tm_themes import.

    Returns
    -------
    dict[str, int | list[int]] : loaded toml file with theme information per algorithm
    """

    theme_name = args.theme
    if theme_name not in tm_themes:
        theme_name = "default"
    return tm_themes[theme_name]


def main():
    args = parse_args()
    theme = get_theme(args)
    maze_algorithm = MAZE_ALGORITHMS[args.maze_algorithm]

    if args.solve_algorithm:
        solve_algorithm = SOLVE_ALGORITHMS[args.solve_algorithm]
    else:
        solve_algorithm = None

    maze = Grid(args.height, args.width, theme[args.maze_algorithm], mask_string=get_mask())
    if not args.seed:
        seed = int().from_bytes(random.randbytes(5), byteorder="big")
    else:
        seed = args.seed
    maze.seed = seed

    try:
        maze_generator = maze_algorithm(maze, theme)
        for maze in maze_generator.generate_maze():
            maze.visual.show(maze_generator.visual_effects, maze_generator.status_text, subject="maze")
        else:
            maze.visual.show(maze_generator.visual_effects, maze_generator.status_text, subject="maze", complete=True)
            print()
        if solve_algorithm:
            solve_generator = solve_algorithm(maze, theme)
            for maze in solve_generator.solve():
                maze.visual.show(solve_generator.visual_effects, solve_generator.status_text, subject="solve")
            else:
                maze.visual.show(
                    solve_generator.visual_effects, solve_generator.status_text, subject="solve", complete=True
                )
                print()

    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


if __name__ == "__main__":
    main()
