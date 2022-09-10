from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
from terminalmaze.tools.visualmaze import Effect
import random
from typing import Union, Generator, Optional


class RecursiveBacktracker(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text: dict[str, Union[Optional[str], Optional[int]]] = {
            "Algorithm": "Recursive Backtracker",
            "Seed": self.maze.seed,
            "Unvisited": "",
            "Stack Length": "",
            "State": "",
        }
        self.skip_frames = 2

    def generate_maze(self) -> Generator[Grid, None, None]:
        cell = self.maze.random_cell()
        stack = [cell]
        ve_stack = Effect(label="multiple", layer=0, color=218, cells=stack)
        self.visual_effects["stack"] = ve_stack
        ve_workingcell = Effect(label="single", layer=1, color=218, cell=cell)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_invalidneighbors = Effect(label="multiple", layer=1, color=52, cells=None)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_lastlinked = Effect(label="single", layer=1, color=218)
        while stack:
            ve_workingcell.cell = cell
            unvisited_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor and not neighbor.links
            ]
            invalid_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor and not neighbor.links
            ]
            self.visual_effects["invalid_neighbors"].cells = invalid_neighbors
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.status_text["State"] = "Walking"
                self.maze.link_cells(cell, next_cell)
                ve_lastlinked.cell = next_cell
                self.visual_effects["last_linked"] = ve_lastlinked
                stack.append(next_cell)
                cell = next_cell
                self.status_text["Unvisited"] = len(unvisited_neighbors)
                self.status_text["Stack Length"] = len(stack)
                yield self.maze

            else:
                stack.pop()
                if stack:
                    self.status_text["State"] = "Backtracking"
                    cell = stack[-1]
                    if self.showlogic:
                        ve_workingcell.cell = cell
                        self.status_text["Stack Length"] = len(stack)
                        if self.frame_wanted():
                            yield self.maze
