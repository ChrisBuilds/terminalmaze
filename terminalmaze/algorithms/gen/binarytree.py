import random
from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from terminalmaze.config import BinaryTreeTheme
from collections.abc import Generator


class BinaryTree(Algorithm):
    def __init__(self, maze: Grid, theme: BinaryTreeTheme):
        super().__init__(maze)
        """
        Create a maze by randomly connecting each cell to its neighbor to the north or east.
        """

        self.status_text["Algorithm"] = "Binary Tree"
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""
        self.theme = theme

    def generate_maze(self) -> Generator[Grid, None, None]:
        unlinked_cells = set(self.maze.each_cell(ignore_mask=True))
        ve_workingcell = ve.ColorSingleCell(self.theme.working_cell)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_neighbor = ve.ColorSingleCell(self.theme.neighbor)
        self.visual_effects["neighbor"] = ve_neighbor
        for cell in self.maze.each_cell(ignore_mask=True):
            ve_workingcell.cell = cell
            neighbors = self.maze.get_neighbors(cell, ignore_mask=True)
            neighbors.pop("south", None)
            neighbors.pop("west", None)
            if neighbors:
                neighbor = random.choice(list(neighbors.values()))
                if neighbor:
                    self.status_text["State"] = "Linking"
                    self.maze.link_cells(cell, neighbor)
                    unlinked_cells.discard(neighbor)
                    unlinked_cells.discard(cell)
                    ve_neighbor.cell = neighbor
            self.status_text["Unlinked Cells"] = len(unlinked_cells)
            yield self.maze

        self.visual_effects.clear()
        self.status_text["State"] = "Complete"
        yield self.maze
