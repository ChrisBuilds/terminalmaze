"""Implements the Hunt and Kill maze generation algorithm.

Hunt and Kill
-------------
Step 1 - Pick a random starting cell.
Step 2 - Randomly walk to unvisited neighbors until a cell with no unvisited neighbors is reached.
Step 3 - Check unvisited cells until a cell with a visited neighbor is discovered.
Step 4 - Repeat steps 2 -> 3 until there are no unvisited cells left.


Classes
-------
    HuntandKill
"""

import random
import time
from collections.abc import Generator

from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import terminalmaze.tools.visualeffects as ve


class HuntandKill(MazeAlgorithm):
    """Implements the Hunt and Kill maze generation algorithm.

    Attributes
    ----------
    grid : Grid
        Grid object from the grid module.
    showlogic : bool
        If True, generate_maze will yield grid more often to allow visualization
        of additional logic.

    Methods
    -------
    generate_maze():
        Generator that yields the Grid when cells are linked and, if showlogic is True,
        when maze logic checks are performed.
    """

    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Hunt And Kill"
        self.frame_time = time.time()

    def generate_maze(self) -> Generator[Grid, None, None]:
        """Generates a maze by linking Cells in a Grid according to the Hunt and Kill maze generation
        algorithm.

        Yields:
            Grid: grid of cells
        """
        unvisited = list(self.maze.each_cell())
        cell = random.choice(unvisited)
        unvisited.remove(cell)
        ve_workingcell = ve.ColorSingleCell(layer=0, cell=cell, color=218)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_lastlinked = ve.ColorSingleCell(layer=0, cell=Cell(0, 0), color=218)
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_invalidneighbors = ve.ColorMultipleCells(layer=0, cells=list(), color=88)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        while unvisited:
            self.status_text["Unvisited Cells"] = len(unvisited)
            ve_workingcell.cell = cell
            unvisited_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor in unvisited
            ]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                self.maze.link_cells(cell, neighbor)
                ve_lastlinked.cell = neighbor
                unvisited.remove(neighbor)
                cell = neighbor
                yield self.maze

            else:
                for cell in unvisited:
                    ve_workingcell.cell = cell
                    neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
                    visited_neighbors = [neighbor for neighbor in neighbors if neighbor.links]
                    ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if not neighbor.links]

                    if self.showlogic:
                        if time.time() - self.frame_time > 0.018:
                            self.frame_time = time.time()
                            yield self.maze
                    if visited_neighbors:
                        ve_invalidneighbors.cells = []
                        neighbor = random.choice(visited_neighbors)
                        self.maze.link_cells(cell, neighbor)
                        ve_lastlinked.cell = neighbor
                        unvisited.remove(cell)
                        yield self.maze
                        break

        yield self.maze
