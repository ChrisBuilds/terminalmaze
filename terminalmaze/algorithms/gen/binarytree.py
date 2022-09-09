import random
from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
from collections.abc import Generator


class BinaryTree(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic=False):
        super().__init__(maze, showlogic)
        """
        Create a maze by randomly connecting each cell to its neighbor to the north or east.
        """

        self.status_text["Algorithm"] = "Binary Tree"

    def generate_maze(self) -> Generator[Grid, None, None]:
        for cell in self.maze.each_cell(ignore_mask=True):
            self.visual_effects["working_cell"] = cell
            neighbors = self.maze.get_neighbors(cell, ignore_mask=True)
            neighbors.pop("south", None)
            neighbors.pop("west", None)
            if neighbors:
                neighbor = random.choice(list(neighbors.values()))
                if neighbor:
                    self.maze.link_cells(cell, neighbor)
                    self.visual_effects["last_linked"] = neighbor
            yield self.maze
