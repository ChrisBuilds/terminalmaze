import random
from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import terminalmaze.tools.visualeffects as ve
from collections.abc import Generator


class BinaryTree(MazeAlgorithm):
    def __init__(self, maze: Grid):
        super().__init__(maze)
        """
        Create a maze by randomly connecting each cell to its neighbor to the north or east.
        """

        self.status_text["Algorithm"] = "Binary Tree"

    def generate_maze(self) -> Generator[Grid, None, None]:
        unlinked_cells = set(self.maze.each_cell(ignore_mask=True))
        ve_workingcell = ve.ColorSingleCell(layer=0, category=ve.LOGIC, cell=Cell(0, 0), color=53)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_neighbor = ve.ColorSingleCell(layer=0, category=ve.LOGIC, cell=Cell(0, 0), color=183)
        self.visual_effects["neighbor"] = ve_neighbor
        for cell in self.maze.each_cell(ignore_mask=True):
            ve_workingcell.cell = cell
            neighbors = self.maze.get_neighbors(cell, ignore_mask=True)
            neighbors.pop("south", None)
            neighbors.pop("west", None)
            if neighbors:
                neighbor = random.choice(list(neighbors.values()))
                if neighbor:
                    self.maze.link_cells(cell, neighbor)
                    unlinked_cells.discard(neighbor)
                    unlinked_cells.discard(cell)
                    ve_neighbor.cell = neighbor
            self.status_text["Unlinked Cells"] = len(unlinked_cells)
            self.status_text["Time Elapsed"] = self.time_elapsed()
            yield self.maze

        self.visual_effects.clear()
        yield self.maze
