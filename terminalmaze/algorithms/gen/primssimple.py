from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import random
from typing import Generator


class PrimsSimple(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Prims Simplified"

    def generate_maze(self) -> Generator[Grid, None, None]:
        cell = self.maze.random_cell()
        edge_cells = list()
        edge_cells.append(cell)
        self.visual_effects["explored"] = edge_cells
        while edge_cells:
            working_cell = edge_cells.pop(random.randrange(len(edge_cells)))
            self.visual_effects["working_cell"] = working_cell
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(working_cell).values() if n and not n.links)
            self.visual_effects["invalid_neighbors"] = list(
                n for n in self.maze.get_neighbors(working_cell).values() if n and n.links
            )
            if unlinked_neighbors:
                next_cell = unlinked_neighbors.pop(random.randrange(len(unlinked_neighbors)))
                self.maze.link_cells(working_cell, next_cell)
                self.visual_effects["last_linked"] = next_cell
                if unlinked_neighbors:
                    edge_cells.append(working_cell)
                unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
                if unlinked_neighbors:
                    edge_cells.append(next_cell)
                yield self.maze
            else:
                if self.showlogic:
                    yield self.maze
