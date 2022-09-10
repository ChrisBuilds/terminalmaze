from terminalmaze.resources.grid import Grid
from terminalmaze.tools.visualeffects import VisualEffect
from typing import Union, Optional, Generator


class SolveAlgorithm:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.visual_effects: dict[str, VisualEffect] = dict()
        self.status_text: dict[str, Union[Optional[str], Optional[int]]] = {"Seed": self.maze.seed}

    def solve(self) -> Generator[Grid, None, None]:
        yield self.maze
