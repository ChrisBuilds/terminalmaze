#!/usr/bin/python3
import argparse
import os
import random
import sys
from argparse import Namespace

import terminalmaze.config as config
from terminalmaze.algorithms.gen.aldousbroder import AldousBroder
from terminalmaze.algorithms.gen.binarytree import BinaryTree
from terminalmaze.algorithms.gen.ellers import Ellers
from terminalmaze.algorithms.gen.huntandkill import HuntandKill
from terminalmaze.algorithms.gen.kruskalsrandomized import KruskalsRandomized
from terminalmaze.algorithms.gen.primssimple import PrimsSimple
from terminalmaze.algorithms.gen.primsweighted import PrimsWeighted
from terminalmaze.algorithms.gen.recursivebacktracker import RecursiveBacktracker
from terminalmaze.algorithms.gen.recursivedivision import RecursiveDivision
from terminalmaze.algorithms.gen.sidewinder import Sidewinder
from terminalmaze.algorithms.gen.wilsons import Wilsons
from terminalmaze.algorithms.solve.breadthfirst import BreadthFirst
from terminalmaze.algorithms.solve.greedybestfirst import GreedyBestFirst
from terminalmaze.resources.grid import Grid

MAZE_ALGORITHMS = {
    "binary_tree": BinaryTree,
    "side_winder": Sidewinder,
    "aldous_broder": AldousBroder,
    "wilsons": Wilsons,
    "hunt_and_kill": HuntandKill,
    "recursive_backtracker": RecursiveBacktracker,
    "recursive_division": RecursiveDivision,
    "prims_simple": PrimsSimple,
    "prims_weighted": PrimsWeighted,
    "kruskals_randomized": KruskalsRandomized,
    "ellers": Ellers,
}

SOLVE_ALGORITHMS = {
    "breadth_first": BreadthFirst,
    "breadth_first_early_exit": BreadthFirst,
    "greedy_best_first": GreedyBestFirst,
}


def parse_args() -> Namespace:
    """
    Parse the arguments passed to at the command line.
    Returns
    -------
    args (argparse.ArgumentParser) : arguments parsed
    """

    maze_algo_help = "\n".join(MAZE_ALGORITHMS.keys())
    solve_algo_help = "\n".join(SOLVE_ALGORITHMS.keys())
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description="Generate and solve mazes in the terminal"
    )
    parser.add_argument(
        "width",
        metavar="WIDTH",
        type=int,
        help="int > 0: Width of the maze grid in characters. Actual width is WIDTH*2. Use 0 for height and width"
        " for auto size.",
    )
    parser.add_argument(
        "height",
        metavar="HEIGHT",
        type=int,
        help="int > 0: Height of the maze grid in lines. Actual height is HEIGHT*2. Use 0 for height and width "
        "for auto size.",
    )
    parser.add_argument(
        "maze_algorithm",
        metavar="MAZE_ALGORITHM",
        type=str,
        help=f"""The maze algorithm used for maze generation. 
Supported Maze Algorithms
-------------------------
{maze_algo_help}""",
        choices=MAZE_ALGORITHMS.keys(),
    )
    parser.add_argument(
        "-sa",
        "--solve_algorithm",
        metavar="ALGORITHM",
        type=str,
        help=f"""The solve algorithm used to solve the maze. 
Supported Solve Algorithms
--------------------------
{solve_algo_help}""",
        required=False,
        default=None,
        choices=list(SOLVE_ALGORITHMS.keys()),
    )
    parser.add_argument(
        "-t",
        "--theme",
        metavar="THEME",
        type=str,
        help="Name of a theme in the themes directory, without the file extension .toml",
        required=False,
        default="default",
    )
    parser.add_argument(
        "-s",
        "--seed",
        metavar="SEED",
        type=int,
        help="Seed to pass to random generator",
        required=False,
        default=None,
    ),
    parser.add_argument(
        "-mk",
        "--mask",
        metavar="MASK",
        type=str,
        help="Name of a mask in the masks directory, without the file extension .mask",
        required=False,
        default=None,
    ),
    parser.add_argument(
        "-mv",
        "--mazeverbosity",
        metavar="MAZEVERBOSITY",
        type=int,
        help="Maze verbosity is a number 0-4 with determines which visual effects are shown. Verbosity is "
        "configurable in theme files. "
        "General practice: 0 = NONE (only status text and final maze), 1 = Maze generation only, 2 = Logic "
        "visual effects, "
        "3 = Style visual effects, 4 = Logic and Style visual effects",
        required=False,
        choices=[0, 1, 2, 3, 4],
        default=3,
    ),
    parser.add_argument(
        "-sv",
        "--solveverbosity",
        metavar="SOLVEVERBOSITY",
        type=int,
        help="Solve verbosity is a number 0-4 with determines which visual effects are shown. Verbosity is "
        "configurable in theme files. "
        "General practice: 0 = NONE (only status text and final maze), 1 = Solve generation only, 2 = Logic "
        "visual effects, "
        "3 = Style visual effects, 4 = Logic and Style visual effects",
        required=False,
        choices=[0, 1, 2, 3, 4],
        default=4,
    ),
    parser.add_argument(
        "--nostatus",
        action="store_true",
        dest="nostatus",
        help="Use to prevent showing status text",
    )
    args = parser.parse_args()
    return args


def get_mask(args) -> str | None:
    """
    Check the masks directory for the configured mask and return the mask as a string.
    Returns
    -------
    str | None : mask string if found, else None
    """
    if args.mask is None:
        return None
    if ".mask" in args.mask:
        mask_name = args.mask.split(".")[0]
    else:
        mask_name = args.mask
    if mask_name in config.tm_masks:
        with open(config.tm_masks[mask_name], "r") as mask_file:
            mask = mask_file.read()
    else:
        mask = None
    return mask


def main():
    args = parse_args()
    maze_algorithm = MAZE_ALGORITHMS[args.maze_algorithm]
    if args.theme in config.themes:
        theme = config.themes[args.theme]
    else:
        print(f"Unable to locate theme: {args.theme}. Verify file exists in themes dir and was spelled correctly.")
        return

    mask = get_mask(args)
    if args.mask and not mask:
        print(f"Unable to locate mask: {args.mask}. Verify file exists in masks dir and was spelled correctly.")
        return

    if args.solve_algorithm:
        solve_algorithm = SOLVE_ALGORITHMS[args.solve_algorithm]
    else:
        solve_algorithm = None

    if args.height == 0 and args.width == 0:
        try:
            columns, lines = os.get_terminal_size()
            width = columns // 2
            height = (lines // 2) - 2  # subtract 2 for the status line
        except OSError:
            print("Unable to determine terminal size. Specify height and width. See -h for usage.")
            return
    else:
        height = args.height
        width = args.width
    maze = Grid(width, height, theme[args.maze_algorithm], mask_string=get_mask(args))
    if not args.seed:
        seed = int().from_bytes(random.randbytes(5), byteorder="big")
    else:
        seed = args.seed
    maze.seed = seed
    mazeverb = args.mazeverbosity
    solveverb = args.solveverbosity
    try:
        maze_generator = maze_algorithm(maze, theme[args.maze_algorithm])
        for maze in maze_generator.generate_maze():
            maze.visual.show(
                maze_generator.visual_effects, maze_generator.status_text, verbosity=mazeverb, nostatus=args.nostatus
            )
        else:
            maze.visual.show(
                maze_generator.visual_effects,
                maze_generator.status_text,
                verbosity=mazeverb,
                complete=True,
                nostatus=args.nostatus,
            )
            print()
        if solve_algorithm:
            conditions = None
            if args.solve_algorithm == "breadth_first_early_exit":
                conditions = "early_exit"
            solve_generator = solve_algorithm(maze, theme[args.solve_algorithm], conditions)
            for maze in solve_generator.solve():
                maze.visual.show(solve_generator.visual_effects, solve_generator.status_text, verbosity=solveverb)
            else:
                maze.visual.show(
                    solve_generator.visual_effects, solve_generator.status_text, verbosity=solveverb, complete=True
                )
                print()

    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.exit()


if __name__ == "__main__":
    main()
