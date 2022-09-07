import random

from grid.grid import Grid
from collections.abc import Generator


class BinaryTree:
    def __init__(self, maze: Grid, showlogic=False):
        """
        Create a maze by randomly connecting each cell to its neighbor to the north or east.
        """

        self.maze = maze
        self.showlogic = showlogic
        self.logic_data = {}
        self.status_text = {"Algorithm": "Binary Tree", "Seed": self.maze.seed}
        random.seed(self.maze.seed)

    def generate_maze(self) -> Generator[Grid, None, None]:
        for cell in self.maze.each_cell(ignore_mask=True):
            self.logic_data["working_cell"] = cell
            neighbors = self.maze.get_neighbors(cell, ignore_mask=True)
            neighbors.pop("south", None)
            neighbors.pop("west", None)
            if neighbors:
                neighbor = random.choice(list(neighbors.values()))
                self.maze.link_cells(cell, neighbor)
                self.logic_data["last_linked"] = neighbor
            yield self.maze
