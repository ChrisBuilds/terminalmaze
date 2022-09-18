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
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve


class HuntandKill(Algorithm):
    """Implements the Hunt and Kill maze generation algorithm.

    Attributes
    ----------
    maze : Grid
        Grid object from the grid module.

    Methods
    -------
    generate_maze():
        Generator that yields the Grid when cells are linked and, if showlogic is True,
        when maze logic checks are performed.
    """

    def __init__(self, maze: Grid, theme: ve.Theme) -> None:
        super().__init__(maze)
        self.status_text["Algorithm"] = "Hunt And Kill"
        self.status_text["Time Elapsed"] = ""
        self.status_text["Unvisited Cells"] = 0
        self.status_text["State"] = ""
        self.link_trail: list[Cell] = []
        self.skip_frames = 3
        self.theme = theme["hunt_and_kill"]

    def generate_maze(self) -> Generator[Grid, None, None]:
        """Generates a maze by linking Cells in a Grid according to the Hunt and Kill maze generation
        algorithm.

        Yields:
            Grid: grid of cells
        """
        unvisited = list(self.maze.each_cell())
        cell = random.choice(unvisited)
        unvisited.remove(cell)
        ve_workingcell = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, cell=cell, color=self.theme["workingcell"]  # type: ignore [arg-type]
        )
        self.visual_effects["working_cell"] = ve_workingcell
        ve_lastlinked = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, cell=Cell(0, 0), color=self.theme["lastlinked"]  # type: ignore [arg-type]
        )
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_invalidneighbors = ve.ColorMultipleCells(
            layer=0, category=ve.LOGIC, cells=list(), color=self.theme["invalidneighbors"]  # type: ignore [arg-type]
        )
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_linktrans = ve.ColorTransition(
            layer=0,
            category=ve.STYLE,
            cells=list(),
            colors=self.theme["linktrans"],
            frames_per_color=2,
            transitioning=dict(),
        )
        self.visual_effects["linktrans"] = ve_linktrans
        ve_hunttrans = ve.ColorTransition(
            layer=0,
            category=ve.STYLE,
            cells=list(),
            colors=self.theme["hunttrans"],
            frames_per_color=2,
            transitioning=dict(),
        )
        self.visual_effects["hunttrans"] = ve_hunttrans

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
                ve_linktrans.cells.append(neighbor)
                ve_lastlinked.cell = neighbor
                unvisited.remove(neighbor)
                cell = neighbor
                self.status_text["Time Elapsed"] = self.time_elapsed()
                yield self.maze

            else:
                for cell in unvisited[:]:
                    self.status_text["State"] = "Hunting"
                    ve_workingcell.cell = cell
                    neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
                    visited_neighbors = [neighbor for neighbor in neighbors if neighbor.links]
                    ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if not neighbor.links]
                    ve_hunttrans.cells.append(cell)
                    if self.frame_wanted():
                        yield self.maze
                    if visited_neighbors:
                        ve_invalidneighbors.cells = []
                        neighbor = random.choice(visited_neighbors)
                        self.maze.link_cells(cell, neighbor)
                        ve_linktrans.cells.append(neighbor)
                        ve_lastlinked.cell = neighbor
                        unvisited.remove(cell)
                        self.status_text["Time Elapsed"] = self.time_elapsed()
                        yield self.maze
                        break

        self.status_text["Unvisited Cells"] = 0
        del self.visual_effects["working_cell"]
        del self.visual_effects["invalid_neighbors"]
        while ve_hunttrans.transitioning:
            self.status_text["Time Elapsed"] = self.time_elapsed()
            yield self.maze
        self.status_text["State"] = "Complete"
        yield self.maze
