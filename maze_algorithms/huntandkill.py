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

from grid.grid import Grid


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
        Generator that yields the Grid when cells are linked and, if showlogic is True,
        when maze logic checks are performed.
    """

    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze = maze
        self.showlogic = showlogic
        self.logic_data = {}
        self.status_text = {"Algorithm": "Hunt And Kill"}
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
        while unvisited:
            self.status_text["Unvisited Cells"] = len(unvisited)
            self.logic_data["working_cell"] = cell
            unvisited_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor in unvisited
            ]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                self.maze.link_cells(cell, neighbor)
                self.logic_data["last_linked"] = neighbor
                unvisited.remove(neighbor)
                cell = neighbor
                yield self.maze

            else:
                for cell in unvisited:
                    self.logic_data["working_cell"] = cell
                    visited_neighbors = [
                        neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor and neighbor.links
                    ]
                    self.logic_data["invalid_neighbors"] = [
                        neighbor
                        for neighbor in self.maze.get_neighbors(cell).values()
                        if neighbor and not neighbor.links
                    ]
                    if self.showlogic:
                        if time.time() - self.frame_time > 0.018:
                            self.frame_time = time.time()
                            yield self.maze
                    if visited_neighbors:
                        self.logic_data["invalid_neighbors"] = []
                        neighbor = random.choice(visited_neighbors)
                        self.maze.link_cells(cell, neighbor)
                        self.logic_data["last_linked"] = neighbor
                        unvisited.remove(cell)
                        yield self.maze
                        break
