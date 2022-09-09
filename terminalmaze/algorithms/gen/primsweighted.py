from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import random
from typing import Generator


class PrimsWeighted(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Prims Weighted"

    def generate_maze(self) -> Generator[Grid, None, None]:
        self.last_linked: list[Cell] = []
        self.visual_effects["last_linked"] = self.last_linked
        cell_weights = {}
        for cell in self.maze.each_cell():
            cell_weights[cell] = random.randint(0, 99)
        cell = self.maze.random_cell()
        links = list()
        unlinked_neighbors = list(n for n in self.maze.get_neighbors(cell).values() if n and not n.links)
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
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
            if unlinked_neighbors:
                for neighbor in unlinked_neighbors:
                    links.append((next_cell, neighbor, cell_weights[neighbor]))
            yield self.maze
