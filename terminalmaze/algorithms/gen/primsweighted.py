from terminalmaze.resources.grid import Grid, Cell
import random
from typing import Union


class PrimsWeighted:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.logic_data: dict[str, Cell] = {}
        self.status_text: dict[str, Union[str, int]] = {"Algorithm": "Prims Weighted", "Seed": self.maze.seed}
        random.seed(self.maze.seed)

    def generate_maze(self) -> Grid:
        self.last_linked = []
        self.logic_data["last_linked"] = self.last_linked
        cell_weights = {}
        for cell in self.maze.each_cell():
            cell_weights[cell] = random.randint(0, 99)
        cell = self.maze.random_cell()
        links = list()
        unlinked_neighbors = list(n for n in self.maze.get_neighbors(cell).values() if not n.links)
        for neighbor in unlinked_neighbors:
            links.append((cell, neighbor, cell_weights[neighbor]))
        while links:
            next_cell: Cell
            working_cell: Cell

            working_cell, next_cell, cost = min(links, key=lambda link: link[2])
            links.remove((working_cell, next_cell, cost))
            if next_cell.links:
                continue
            self.maze.link_cells(working_cell, next_cell)
            self.last_linked.append(next_cell)
            if len(self.last_linked) == 10:
                self.last_linked.pop(0)
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if not n.links)
            if unlinked_neighbors:
                for neighbor in unlinked_neighbors:
                    links.append((next_cell, neighbor, cell_weights[neighbor]))
            yield self.maze
