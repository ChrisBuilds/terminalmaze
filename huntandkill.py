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

from grid import Grid
import random


class HuntandKill:
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
        Generator the yields the Grid when cells are linked and, if showlogic is True,
        when maze logic checks are performed.
    """

    def __init__(self, grid: Grid, showlogic=False):
        self.grid = grid
        self.logic_data = {}

    def generate_maze(self):
        """Generates a maze by linking Cells in a Grid according to the Hunt and Kill maze generation
        algorithm.

        Yields:
            Grid: grid of cells
        """
        unvisited = [cell for cell in self.grid.cells.values()]
        cell = random.choice(unvisited)
        unvisited.remove(cell)
        while unvisited:
            self.logic_data["working_cell"] = cell
            unvisited_neighbors = [c for c in self.grid.get_neighbors(cell) if c in unvisited]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                cell.link(neighbor)
                self.logic_data["last_linked"] = neighbor
                unvisited.remove(neighbor)
                cell = neighbor
                yield self.grid

            else:
                for cell in unvisited:
                    self.logic_data["working_cell"] = cell
                    visited_neighbors = [c for c in self.grid.get_neighbors(cell) if c not in unvisited]
                    yield self.grid
                    if visited_neighbors:
                        neighbor = random.choice(visited_neighbors)
                        cell.link(neighbor)
                        self.logic_data["last_linked"] = neighbor
                        unvisited.remove(cell)
                        break
                yield self.grid
