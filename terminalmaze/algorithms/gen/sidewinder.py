import random
from collections.abc import Generator

from terminalmaze.resources.grid import Grid
from terminalmaze.resources.cell import Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from terminalmaze.config import SideWinderTheme


class Sidewinder(Algorithm):
    def __init__(self, maze: Grid, theme: SideWinderTheme):
        """
        For each row, randomly link cells in a run of cells to their north or east neighbor.
        """
        super().__init__(maze)
        self.theme = theme
        self.status_text["Algorithm"] = "Sidewinder"
        self.status_text["Unvisited Cells"] = 0
        self.status_text["State"] = ""

    def generate_maze(self) -> Generator[Grid, None, None]:
        run: list[Cell] = []
        ve_run = ve.ColorMultipleCells(ve.LOGIC, self.theme.run)
        ve_run.cells = run
        self.visual_effects["run"] = ve_run

        ve_workingcell = ve.ColorSingleCell(ve.LOGIC, self.theme.working_cell)
        self.visual_effects["working_cell"] = ve_workingcell

        ve_lastlinked = ve.ColorSingleCell(ve.LOGIC, self.theme.last_linked)
        self.visual_effects["last_linked"] = ve_lastlinked

        total_cells_unvisited = len(list(self.maze.each_cell(ignore_mask=True)))
        self.status_text["Unvisited Cells"] = total_cells_unvisited

        for row in self.maze.each_row(ignore_mask=True, bottom_up=True):
            unvisited_cells = row.copy()
            while unvisited_cells:
                working_cell = unvisited_cells.pop(0)
                total_cells_unvisited -= 1
                self.status_text["Unvisited Cells"] = total_cells_unvisited
                ve_workingcell.cell = working_cell
                run.append(working_cell)
                while run:
                    self.status_text["State"] = "Run"
                    neighbors = self.maze.get_neighbors(working_cell, ignore_mask=True)
                    if "west" in neighbors:
                        del neighbors["west"]
                    if "south" in neighbors:
                        del neighbors["south"]
                    if not neighbors:
                        break
                    direction = random.choice(list(neighbors.keys()))
                    if direction == "east" and neighbors["east"]:
                        self.maze.link_cells(working_cell, neighbors["east"])
                        ve_lastlinked.cell = neighbors["east"]
                        working_cell = neighbors["east"]
                        ve_workingcell.cell = working_cell
                        run.append(working_cell)
                        unvisited_cells.pop(0)
                    elif direction == "north":
                        self.status_text["State"] = "Climb"
                        working_cell = random.choice(run)
                        ve_workingcell.cell = working_cell
                        neighbor_north = self.maze.get_neighbors(working_cell, ignore_mask=True)["north"]
                        if neighbor_north:
                            self.maze.link_cells(working_cell, neighbor_north)
                            ve_lastlinked.cell = neighbor_north
                        run.clear()
                    yield self.maze
        self.visual_effects.clear()
        self.status_text["State"] = "Complete"
        yield self.maze
