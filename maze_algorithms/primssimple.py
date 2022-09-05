from grid.grid import Grid, Cell
import random
from typing import Union


class PrimsSimple:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.logic_data: dict[str, Cell] = {}
        self.status_text: dict[str, Union[str, int]] = {"Algorithm": "Prims Simplified"}

    def generate_maze(self) -> Grid:
        cell = self.maze.random_cell()
        edge_cells = list()
        edge_cells.append(cell)
        self.logic_data["explored"] = edge_cells
        while edge_cells:
            working_cell = edge_cells.pop(random.randrange(len(edge_cells)))
            self.logic_data["working_cell"] = working_cell
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(working_cell).values() if not n.links)
            self.logic_data["invalid_neighbors"] = list(
                n for n in self.maze.get_neighbors(working_cell).values() if n.links
            )
            if unlinked_neighbors:
                next_cell = unlinked_neighbors.pop(random.randrange(len(unlinked_neighbors)))
                self.maze.link_cells(working_cell, next_cell)
                self.logic_data["last_linked"] = next_cell
                if unlinked_neighbors:
                    edge_cells.append(working_cell)
                unlinked_neighbors = set(n for n in self.maze.get_neighbors(next_cell).values() if not n.links)
                if unlinked_neighbors:
                    edge_cells.append(next_cell)
                yield self.maze
            else:
                yield self.maze
