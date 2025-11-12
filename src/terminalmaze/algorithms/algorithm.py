import random
import time
from typing import Generator

from pydantic import BaseModel

from terminalmaze.resources.grid import Cell, Grid
from terminalmaze.visual.visualeffects import VisualEffect


class Algorithm:
    def __init__(self, maze: Grid, theme: BaseModel) -> None:
        self.maze: Grid = maze
        self.theme = theme
        self.visual_effects: dict[str, VisualEffect] = dict()
        self.status_text: dict[str, str | int | None] = dict()
        self.status_text = {"Algorithm": "", "Seed": self.maze.seed, "Time Elapsed": ""}
        self.skip_frames = 0
        self.frames_skipped = 0
        self.start_time = time.time()
        random.seed(self.maze.seed)

    @staticmethod
    def distance(position: Cell, target: Cell) -> int:
        return abs(position.row - target.row) + abs(position.column - target.column)

    def generate_maze(self) -> Generator[Grid, None, None]:
        """
        Generate a maze by linking cells in the Grid.
        """
        yield self.maze

    def frame_wanted_relative(self, relative_to: list[Cell] | None, divisor: int = 1) -> bool:
        """Skip frames relative to the length of a list of Cells. Used to avoid slowdowns in algorithms
        that have many 'ends' or workingcells alternative paths.

        Args:
            relative_to (list[Cell]): List of cells on which to base the frame skip.
            divisor (int): relative to // divisor, used to reduce the number of skipped frames for tuning.
            Defaults to 1.

        Returns:
            bool: True if frame should be displayed, else False.
        """

        if not isinstance(relative_to, list):
            raise TypeError(relative_to)
        if not divisor >= 1 and isinstance(divisor, int):
            raise ValueError(divisor)

        skip_frames_now = len(relative_to) // divisor
        if self.frames_skipped >= self.skip_frames:
            self.frames_skipped = 0
            self.skip_frames = skip_frames_now
            return True
        # adjust skip_frames if relative_to length drops below frames_skipped between shown frames
        elif self.skip_frames > skip_frames_now:
            self.skip_frames = skip_frames_now
            if self.frames_skipped > self.skip_frames:
                self.frames_skipped = 0
                return True
        else:
            self.frames_skipped += 1
            return False

        return True

    def frame_wanted(self) -> bool:
        """Return True if the number of frames skipped is equal to the
        self.skip_frames variable.

        Returns:
            bool: True if self.frames_skipped == self.skip_frames, else False.
        """
        if self.skip_frames == 0:
            return True
        if self.frames_skipped >= self.skip_frames:
            self.frames_skipped = 0
            return True
        else:
            self.frames_skipped += 1
            return False
