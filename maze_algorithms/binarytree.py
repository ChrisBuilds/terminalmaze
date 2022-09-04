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

    def generate_maze(self) -> Generator[Grid, None, None]:
        for cell in self.maze.each_cell():
            self.logic_data["working_cell"] = cell
            neighbors = []
            for direction in ("north", "east"):
                if cell.neighbors.get(direction):
                    neighbors.append(cell.neighbors.get(direction))
            if neighbors:
                neighbor = random.choice(neighbors)
                cell.link(neighbor)
                self.logic_data["last_linked"] = neighbor
            yield self.maze
