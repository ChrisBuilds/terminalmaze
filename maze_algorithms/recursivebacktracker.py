from grid.grid import Grid, Cell
import random
from typing import Union


class RecursiveBacktracker:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.logic_data: dict[str, Cell] = {}
        self.status_text: dict[str, Union[str, int]] = {"Algorithm": "Recursive Backtracker", "Seed": self.maze.seed}
        self.frame_delay = 3
        random.seed(self.maze.seed)

    def generate_maze(self) -> Grid:
        cell = self.maze.random_cell()
        stack = [cell]
        self.logic_data["explored"] = stack
        while stack:
            self.logic_data["working_cell"] = cell
            unvisited_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if not neighbor.links
            ]
            self.logic_data["invalid_neighbors"] = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor.links
            ]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.maze.link_cells(cell, next_cell)
                self.logic_data["last_linked"] = next_cell
                stack.append(next_cell)
                cell = next_cell
                self.status_text["Unvisited"] = len(unvisited_neighbors)
                self.status_text["Stack Length"] = len(stack)
                yield self.maze

            else:
                stack.pop()
                if stack:
                    cell = stack[-1]
                    if self.showlogic:
                        self.logic_data["working_cell"] = cell
                        self.status_text["Stack Length"] = len(stack)
                        self.frame_delay -= 1
                        if self.frame_delay == 0:
                            self.frame_delay = 3
                            yield self.maze
