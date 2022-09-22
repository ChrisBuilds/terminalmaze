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
from collections.abc import Generator

from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from terminalmaze.config import HuntAndKillTheme


class HuntandKill(Algorithm):
    """Implements the Hunt and Kill maze generation algorithm.

    Methods
    -------
    generate_maze():
        Generator that yields the Grid when cells are linked and, if showlogic is True,
        when maze logic checks are performed.
    """

    def __init__(self, maze: Grid, theme: HuntAndKillTheme) -> None:
        """Implements the Hunt and Kill maze generation algorithm.

        Attributes
        ----------
        maze : Grid
            Grid object from the grid module.
        """
        super().__init__(maze)
        self.status_text["Algorithm"] = "Hunt And Kill"
        self.status_text["Unvisited Cells"] = 0
        self.status_text["State"] = ""
        self.link_trail: list[Cell] = []
        self.skip_frames = 3
        self.theme = theme

    def generate_maze(self) -> Generator[Grid, None, None]:
        """Generates a maze by linking Cells in a Grid according to the Hunt and Kill maze generation
        algorithm.

        Yields:
            Grid: grid of cells
        """
        unvisited = list(self.maze.each_cell())
        cell = random.choice(unvisited)
        unvisited.remove(cell)
        ve_workingcell = ve.ColorSingleCell(self.theme.working_cell)
        ve_workingcell.cell = cell
        self.visual_effects["working_cell"] = ve_workingcell

        ve_lastlinked = ve.ColorSingleCell(self.theme.last_linked)
        self.visual_effects["last_linked"] = ve_lastlinked

        ve_invalidneighbors = ve.ColorMultipleCells(self.theme.invalid_neighbors)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors

        ve_link_transition = ve.ValueTransition(self.theme.link_transition)
        self.visual_effects["linktrans"] = ve_link_transition

        ve_hunt_transition = ve.ValueTransition(self.theme.hunt_transition)
        self.visual_effects["hunttrans"] = ve_hunt_transition

        while unvisited:
            self.status_text["Unvisited Cells"] = len(unvisited)
            ve_workingcell.cell = cell
            unvisited_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor in unvisited
            ]
            if unvisited_neighbors:
                self.status_text["State"] = "Linking"
                neighbor = random.choice(unvisited_neighbors)
                self.maze.link_cells(cell, neighbor)
                ve_link_transition.cells.append(neighbor)
                ve_lastlinked.cell = neighbor
                unvisited.remove(neighbor)
                cell = neighbor
                yield self.maze

            else:
                for cell in unvisited[:]:
                    self.status_text["State"] = "Hunting"
                    ve_workingcell.cell = cell
                    neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
                    visited_neighbors = [neighbor for neighbor in neighbors if neighbor.links]
                    ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if not neighbor.links]
                    ve_hunt_transition.cells.append(cell)
                    if self.frame_wanted():
                        yield self.maze
                    if visited_neighbors:
                        ve_invalidneighbors.cells = []
                        neighbor = random.choice(visited_neighbors)
                        self.maze.link_cells(cell, neighbor)
                        ve_link_transition.cells.append(neighbor)
                        ve_lastlinked.cell = neighbor
                        unvisited.remove(cell)
                        yield self.maze
                        break

        self.status_text["Unvisited Cells"] = 0
        del self.visual_effects["working_cell"]
        del self.visual_effects["invalid_neighbors"]
        while ve_hunt_transition.transitioning:
            yield self.maze
        self.status_text["State"] = "Complete"
        yield self.maze
