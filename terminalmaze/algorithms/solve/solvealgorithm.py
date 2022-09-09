from terminalmaze.resources.grid import Grid, Cell
from typing import Union, Optional, Generator, DefaultDict


class SolveAlgorithm:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.visual_effects: dict[
            str, Union[Cell, list[Cell], dict[int, Cell], DefaultDict[int, list[Cell]], DefaultDict[int, set[Cell]]]
        ] = {}
        self.status_text: dict[str, Union[Optional[str], Optional[int]]] = {"Seed": self.maze.seed}

    def solve(self) -> Generator[Grid, None, None]:
        yield self.maze
