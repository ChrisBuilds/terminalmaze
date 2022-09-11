import random
from collections.abc import Generator

from terminalmaze.resources.grid import Grid
from terminalmaze.resources.cell import Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import terminalmaze.tools.visualeffects as ve


class Sidewinder(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False):
        """
        For each row, randomly link cells in a run of cells to their north or east neighbor.
        """
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Sidewinder"
        self.status_text["Seed"] = self.maze.seed

    def generate_maze(self) -> Generator[Grid, None, None]:
        run: list[Cell] = []
        ve_run = ve.ColorMultipleCells(layer=0, cells=run, color=218)
        self.visual_effects["run"] = ve_run
        ve_workingcell = ve.ColorSingleCell(layer=0, cell=Cell(0, 0), color=218)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_lastlinked = ve.ColorSingleCell(layer=0, cell=Cell(0, 0), color=159)
        self.visual_effects["last_linked"] = ve_lastlinked

        for row in self.maze.each_row(ignore_mask=True, bottom_up=True):
            unvisited_cells = row.copy()
            while unvisited_cells:
                working_cell = unvisited_cells.pop(0)
                ve_workingcell.cell = working_cell
                run.append(working_cell)
                while run:
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
                        working_cell = random.choice(run)
                        ve_workingcell.cell = working_cell
                        neighbor_north = self.maze.get_neighbors(working_cell, ignore_mask=True)["north"]
                        if neighbor_north:
                            self.maze.link_cells(working_cell, neighbor_north)
                            ve_lastlinked.cell = neighbor_north
                        run.clear()
                    self.status_text["Time Elapsed"] = self.time_elapsed()
                    yield self.maze
