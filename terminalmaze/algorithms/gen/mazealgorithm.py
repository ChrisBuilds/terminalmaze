from terminalmaze.resources.grid import Grid, Cell
import random
from typing import Union


class MazeAlgorithm:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.visual_effects: dict[str, Union[Cell, list[Cell], dict[int, Cell]]] = {}
        self.status_text: dict[str, Union[str, int]] = {}
        self.skip_frames = 0
        self.frames_skipped = 0
        random.seed(self.maze.seed)

    def generate_maze(self) -> Grid:
        pass

    def frame_wanted(self) -> bool:
        """Return True of the number of frames skipped is equal to the
        self.skip_frames variable.

        Returns:
            bool: True if self.frames_skipped == self.skip_frames, else False.
        """
        if not self.skip_frames:
            return True
        if self.frames_skipped == self.skip_frames:
            self.frames_skipped = 0
            return True
        else:
            self.frames_skipped += 1
            return False
