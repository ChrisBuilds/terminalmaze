from terminalmaze.resources.grid import Grid
from terminalmaze.tools.visualeffects import VisualEffect
import random
import time
from typing import Generator


class MazeAlgorithm:
    def __init__(self, maze: Grid) -> None:
        self.maze: Grid = maze
        self.visual_effects: dict[str, VisualEffect] = dict()
        self.status_text: dict[str, str | int | None] = dict()
        self.status_text = {"Algorithm": "", "Seed": self.maze.seed, "Time Elapsed": ""}
        self.skip_frames = -1
        self.frames_skipped = -1
        self.start_time = time.time()
        random.seed(self.maze.seed)

    def generate_maze(self) -> Generator[Grid, None, None]:
        """
        Generate a maze by linking cells in the Grid.
        """
        yield self.maze

    def frame_wanted(self) -> bool:
        """Return True of the number of frames skipped is equal to the
        self.skip_frames variable.

        Returns:
            bool: True if self.frames_skipped == self.skip_frames, else False.
        """
        if self.skip_frames < 0:
            return True
        if self.frames_skipped == self.skip_frames:
            self.frames_skipped = 0
            return True
        else:
            self.frames_skipped += 1
            return False

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
