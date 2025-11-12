import random
from collections.abc import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import BinaryTreeTheme
from terminalmaze.resources.grid import Grid


class BinaryTree(Algorithm):
    def __init__(self, maze: Grid, theme: BinaryTreeTheme):
        super().__init__(maze, theme)
        """
        Create a maze by randomly connecting each cell to its neighbor to the north or east.
        """

        self.status_text["Algorithm"] = "Binary Tree"
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""
        self.theme = theme

    def generate_maze(self) -> Generator[Grid, None, None]:
        unlinked_cells = set(self.maze.each_cell(ignore_mask=True))

        ve_workingcell = ve.Animation(self.theme.working_cell)
        self.visual_effects["working_cell"] = ve_workingcell

        ve_last_linked = ve.Animation(self.theme.last_linked)
        self.visual_effects["last_linked"] = ve_last_linked

        ve_neighbors = ve.Animation(self.theme.neighbors)
        self.visual_effects["neighbors"] = ve_neighbors

        for cell in self.maze.each_cell(ignore_mask=True):
            ve_workingcell.cells.append(cell)
            neighbors = self.maze.get_neighbors(cell, ignore_mask=True)
            ve_neighbors.cells.extend([cell for cell in neighbors.values()])
            neighbors.pop("south", None)
            neighbors.pop("west", None)
            if neighbors:
                neighbor = random.choice(list(neighbors.values()))
                if neighbor:
                    self.status_text["State"] = "Linking"
                    self.maze.link_cells(cell, neighbor)
                    unlinked_cells.discard(neighbor)
                    unlinked_cells.discard(cell)
                    ve_last_linked.cells.append(neighbor)
            self.status_text["Unlinked Cells"] = len(unlinked_cells)
            yield self.maze

        self.visual_effects.clear()
        self.status_text["State"] = "Complete"
        yield self.maze
