import argparse
import random
import shutil
import sys

import terminalmaze.algorithms.gen as maze_algos
import terminalmaze.algorithms.solve as solve_algos
import terminalmaze.config as config
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.resources.grid import Grid
from terminalmaze.visual import ansitools

MAZE_ALGORITHMS: dict[str, type[Algorithm]] = {
    "binary_tree": maze_algos.binarytree.BinaryTree,
    "side_winder": maze_algos.sidewinder.Sidewinder,
    "aldous_broder": maze_algos.aldousbroder.AldousBroder,
    "wilsons": maze_algos.wilsons.Wilsons,
    "hunt_and_kill": maze_algos.huntandkill.HuntandKill,
    "recursive_backtracker": maze_algos.recursivebacktracker.RecursiveBacktracker,
    "recursive_division": maze_algos.recursivedivision.RecursiveDivision,
    "prims_simple": maze_algos.primssimple.PrimsSimple,
    "prims_weighted": maze_algos.primsweighted.PrimsWeighted,
    "kruskals_randomized": maze_algos.kruskalsrandomized.KruskalsRandomized,
    "ellers": maze_algos.ellers.Ellers,
}

SOLVE_ALGORITHMS: dict[str, type[Algorithm]] = {
    "breadth_first": solve_algos.breadthfirst.BreadthFirst,
    "breadth_first_early_exit": solve_algos.breadthfirst.BreadthFirst,
    "greedy_best_first": solve_algos.greedybestfirst.GreedyBestFirst,
}


def parse_args() -> argparse.Namespace:
    """
    Parse the arguments passed to at the command line.
    Returns
    -------
    args (argparse.Namespace) : arguments parsed
    """

    maze_algo_help = "\n".join(MAZE_ALGORITHMS.keys())
    solve_algo_help = "\n".join(SOLVE_ALGORITHMS.keys())
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Generate and solve mazes in the terminal",
    )
    parser.add_argument(
        "width",
        metavar="WIDTH",
        type=int,
        help="int >= 0: Width of the maze grid in characters. Actual width is WIDTH*2. Use 0 for height and width"
        " for auto size.",
    )
    parser.add_argument(
        "height",
        metavar="HEIGHT",
        type=int,
        help="int >= 0: Height of the maze grid in lines. Actual height is HEIGHT*2. Use 0 for height and width "
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
        default=None,
        choices=list(SOLVE_ALGORITHMS.keys()),
    )
    parser.add_argument(
        "-t",
        "--theme",
        metavar="THEME",
        type=str,
        help="Name of a theme in the themes directory, without the file extension .toml",
        default="default",
    )
    parser.add_argument(
        "-s",
        "--seed",
        metavar="SEED",
        type=int,
        help="Seed to pass to random generator",
        default=None,
    )
    parser.add_argument(
        "-mk",
        "--mask",
        metavar="MASK",
        type=str,
        help="Name of a mask in the masks directory, without the file extension .mask",
        default=None,
    )
    parser.add_argument(
        "-mv",
        "--maze_verbosity",
        metavar="MAZEVERBOSITY",
        type=int,
        help="Maze verbosity is a number 0-4 with determines which visual effects are shown. Verbosity is "
        "configurable in theme files. "
        "General practice: 0 = NONE (only status text and final maze), 1 = Maze generation only, 2 = Logic "
        "visual effects, "
        "3 = Style visual effects, 4 = Logic and Style visual effects",
        choices=[0, 1, 2, 3, 4],
        default=3,
    )
    parser.add_argument(
        "-sv",
        "--solve_verbosity",
        metavar="SOLVEVERBOSITY",
        type=int,
        help="Solve verbosity is a number 0-4 with determines which visual effects are shown. Verbosity is "
        "configurable in theme files. "
        "General practice: 0 = NONE (only status text and final maze), 1 = Solve generation only, 2 = Logic "
        "visual effects, "
        "3 = Style visual effects, 4 = Logic and Style visual effects",
        choices=[0, 1, 2, 3, 4],
        default=4,
    )
    parser.add_argument(
        "-rd",
        "--redraw_delay",
        metavar="REDRAW",
        type=float,
        help="The minimum time, in seconds, between screen redraws. This controls the speed of the animation. Default = 0.015",
        default=0.015,
    )
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


def _get_terminal_dimensions() -> tuple[int, int]:
    """Gets the terminal dimensions.

    Returns:
        tuple[int, int]: terminal width and height
    """
    try:
        terminal_width, terminal_height = shutil.get_terminal_size()
    except OSError:
        print("Unable to determine terminal size. Specify height and width. See -h for usage.")
        return (0, 0)
    return terminal_width, terminal_height


def main():
    args = parse_args()
    maze_algorithm = MAZE_ALGORITHMS[args.maze_algorithm]
    if args.solve_algorithm:
        solve_algorithm = SOLVE_ALGORITHMS[args.solve_algorithm]
    else:
        solve_algorithm = None
    if args.theme in config.themes:
        theme = config.themes[args.theme]
        if ma := args.maze_algorithm:
            if ma not in theme:
                print(f"Unable to locate theme specification for maze algorithm ({ma}) in theme file ({args.theme}).")
                return
        if sa := args.solve_algorithm:
            if sa not in theme:
                print(f"Unable to locate theme specification for solve algorithm ({sa}) in theme file ({args.theme}).")
                return
    else:
        print(f"Unable to locate theme: {args.theme}. Verify file exists in themes dir and was spelled correctly.")
        return

    mask = get_mask(args)
    if args.mask and not mask:
        print(f"Unable to locate mask: {args.mask}. Verify file exists in masks dir and was spelled correctly.")
        return

    if args.height == 0 and args.width == 0:
        columns, lines = _get_terminal_dimensions()
        width = (columns // 2) - 1  # subtract 1 for the maze border wall
        height = (lines // 2) - 1  # subtract 2 for the status line

    else:
        height = args.height
        width = args.width
    maze = Grid(width, height, theme[args.maze_algorithm], mask_string=get_mask(args))
    if not args.seed:
        seed = int().from_bytes(random.randbytes(5), byteorder="big")
    else:
        seed = args.seed
    maze.seed = seed
    mazeverb = args.maze_verbosity
    solveverb = args.solve_verbosity
    try:
        maze_generator = maze_algorithm(maze, theme[args.maze_algorithm])
        for maze in maze_generator.generate_maze():
            maze.visual.show(
                maze_generator.visual_effects,
                maze_generator.status_text,
                verbosity=mazeverb,
                nostatus=args.nostatus,
                redrawdelay=args.redraw_delay,
            )
        else:
            maze.visual.show(
                maze_generator.visual_effects,
                maze_generator.status_text,
                verbosity=mazeverb,
                complete=True,
                nostatus=args.nostatus,
                redrawdelay=args.redraw_delay,
            )
            print()
        if solve_algorithm:
            conditions = None
            if args.solve_algorithm == "breadth_first_early_exit":
                conditions = "early_exit"
            solve_generator = solve_algorithm(maze, theme[args.solve_algorithm], conditions)
            for maze in solve_generator.solve():
                maze.visual.show(
                    solve_generator.visual_effects,
                    solve_generator.status_text,
                    nostatus=args.nostatus,
                    verbosity=solveverb,
                    redrawdelay=args.redraw_delay,
                )
            else:
                maze.visual.show(
                    solve_generator.visual_effects,
                    solve_generator.status_text,
                    verbosity=solveverb,
                    nostatus=args.nostatus,
                    complete=True,
                    redrawdelay=args.redraw_delay,
                )
                print()
        sys.stdout.write(ansitools.SHOW_CURSOR())
    except KeyboardInterrupt:
        print("Maze generation stopped.")
        sys.stdout.write(ansitools.SHOW_CURSOR())
        sys.exit()


if __name__ == "__main__":
    main()
