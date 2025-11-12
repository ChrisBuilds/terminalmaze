import random
from collections import deque
from collections.abc import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import SideWinderTheme
from terminalmaze.resources.cell import Cell
from terminalmaze.resources.grid import Grid


class Sidewinder(Algorithm):
    def __init__(self, maze: Grid, theme: SideWinderTheme):
        """
        For each row, randomly link cells in a run of cells to their north or east neighbor.
        """
        super().__init__(maze, theme)
        self.theme = theme
        self.status_text["Algorithm"] = "Sidewinder"
        self.status_text["Unvisited Cells"] = 0
        self.status_text["State"] = ""

    def generate_maze(self) -> Generator[Grid, None, None]:
        ve_run = ve.ModifyMultipleCells(self.theme.run)
        self.visual_effects["run"] = ve_run

        ve_working_cell = ve.Animation(self.theme.working_cell)
        self.visual_effects["working_cell"] = ve_working_cell

        ve_last_linked = ve.Animation(self.theme.last_linked)
        self.visual_effects["last_linked"] = ve_last_linked

        total_cells_unvisited = len(list(self.maze.each_cell(ignore_mask=True)))
        self.status_text["Unvisited Cells"] = total_cells_unvisited

        run: list[Cell] = []
        ve_run.cells = run
        unvisited_cells: deque = deque()
        for row in self.maze.each_row(ignore_mask=True, bottom_up=True):
            unvisited_cells.extend(row.copy())
            while unvisited_cells:
                working_cell = unvisited_cells.popleft()
                total_cells_unvisited -= 1
                self.status_text["Unvisited Cells"] = total_cells_unvisited
                ve_working_cell.cells.append(working_cell)
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
                        ve_last_linked.cells.append(neighbors["east"])
                        working_cell = neighbors["east"]
                        ve_working_cell.cells.append(working_cell)
                        run.append(working_cell)
                        unvisited_cells.popleft()
                    elif direction == "north":
                        self.status_text["State"] = "Climb"
                        working_cell = random.choice(run)
                        ve_working_cell.cells.append(working_cell)
                        neighbor_north = self.maze.get_neighbors(working_cell, ignore_mask=True)["north"]
                        if neighbor_north:
                            self.maze.link_cells(working_cell, neighbor_north)
                            ve_last_linked.cells.append(neighbor_north)
                        run.clear()
                    yield self.maze
        self.visual_effects.clear()
        self.status_text["State"] = "Complete"
        yield self.maze
