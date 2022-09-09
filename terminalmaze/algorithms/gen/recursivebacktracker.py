from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
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
        self.visual_effects["explored"] = stack
        while stack:
            self.visual_effects["working_cell"] = cell
            unvisited_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor and not neighbor.links
            ]
            self.visual_effects["invalid_neighbors"] = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor and not neighbor.links
            ]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.status_text["State"] = "Walking"
                self.maze.link_cells(cell, next_cell)
                self.visual_effects["last_linked"] = next_cell
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
                        self.visual_effects["working_cell"] = cell
                        self.status_text["Stack Length"] = len(stack)
                        if self.frame_wanted:
                            yield self.maze
