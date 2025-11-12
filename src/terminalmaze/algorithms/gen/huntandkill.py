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

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import HuntAndKillTheme
from terminalmaze.resources.grid import Cell, Grid


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
        super().__init__(maze, theme)
        self.status_text["Algorithm"] = "Hunt And Kill"
        self.status_text["Unvisited Cells"] = 0
        self.status_text["State"] = ""
        self.link_trail: list[Cell] = []
        self.skip_frames = theme.hunting_frames_skip
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

        ve_workingcell = ve.Animation(self.theme.working_cell)
        ve_workingcell.cells.append(cell)
        self.visual_effects["working_cell"] = ve_workingcell

        ve_invalidneighbors = ve.Animation(self.theme.invalid_neighbors)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors

        ve_last_linked = ve.Animation(self.theme.last_linked)
        self.visual_effects["linktrans"] = ve_last_linked

        ve_hunt_cells = ve.Animation(self.theme.hunt_cells)
        self.visual_effects["hunttrans"] = ve_hunt_cells

        while unvisited:
            self.status_text["Unvisited Cells"] = len(unvisited)
            ve_workingcell.cells.append(cell)
            unvisited_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor in unvisited
            ]
            if unvisited_neighbors:
                self.status_text["State"] = "Linking"
                neighbor = random.choice(unvisited_neighbors)
                self.maze.link_cells(cell, neighbor)
                ve_last_linked.cells.append(neighbor)
                unvisited.remove(neighbor)
                cell = neighbor
                yield self.maze

            else:
                for cell in unvisited[:]:
                    self.status_text["State"] = "Hunting"
                    ve_workingcell.cells.append(cell)
                    neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
                    visited_neighbors = [neighbor for neighbor in neighbors if neighbor.links]
                    ve_invalidneighbors.cells.extend([neighbor for neighbor in neighbors if not neighbor.links])
                    ve_hunt_cells.cells.append(cell)
                    if self.frame_wanted():
                        yield self.maze
                    if visited_neighbors:
                        neighbor = random.choice(visited_neighbors)
                        self.maze.link_cells(cell, neighbor)
                        ve_last_linked.cells.append(neighbor)
                        unvisited.remove(cell)
                        yield self.maze
                        break

        self.status_text["Unvisited Cells"] = 0
        del self.visual_effects["working_cell"]
        del self.visual_effects["invalid_neighbors"]
        while (
            ve_hunt_cells.animating
            or ve_invalidneighbors.animating
            or ve_last_linked.animating
            or ve_workingcell.animating
        ):
            yield self.maze
        self.status_text["State"] = "Complete"
        yield self.maze
