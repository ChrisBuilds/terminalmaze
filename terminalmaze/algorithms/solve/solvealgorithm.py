from terminalmaze.resources.grid import Grid
from terminalmaze.tools.visualeffects import VisualEffect
import time
from typing import Union, Optional, Generator


class SolveAlgorithm:
    def __init__(self, maze: Grid) -> None:
        self.maze: Grid = maze
        self.visual_effects: dict[str, VisualEffect] = dict()
        self.status_text: dict[str, Union[Optional[str], Optional[int]]]
        self.status_text = {"Algorithm": "", "Seed": self.maze.seed, "Time Elapsed": ""}
        self.start_time = time.time()

    def solve(self) -> Generator[Grid, None, None]:
        yield self.maze

    def time_elapsed(self) -> str:
        """
        Calculate the run time in minutes/seconds and return string representation.
        Returns
        -------
        str : Time in format {minutes}m {seconds}s
        """
        seconds = time.time() - self.start_time
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}m {seconds}s"
