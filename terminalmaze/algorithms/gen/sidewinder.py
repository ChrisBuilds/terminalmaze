import random
from collections.abc import Generator

from terminalmaze.resources.grid import Grid
from terminalmaze.resources.cell import Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm


class Sidewinder(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False):
        """
        For each row, randomly link cells in a run of cells to their north or east neighbor.
        """
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Sidewinder"

    def generate_maze(self) -> Generator[Grid, None, None]:
        run: list[Cell] = []
        self.visual_effects["logic0"] = run
        for row in self.maze.each_row(ignore_mask=True, bottom_up=True):
            unvisited_cells = row.copy()
            while unvisited_cells:
                working_cell = unvisited_cells.pop(0)
                self.visual_effects["working_cell"] = working_cell
                run.append(working_cell)
                while run:
                    neighbors = {}
                    if "north" in self.maze.get_neighbors(working_cell, ignore_mask=True):
                        neighbors["north"] = self.maze.get_neighbors(working_cell, ignore_mask=True)["north"]
                    if "east" in self.maze.get_neighbors(working_cell, ignore_mask=True):
                        neighbors["east"] = self.maze.get_neighbors(working_cell, ignore_mask=True)["east"]
                    if not neighbors:
                        break
                    direction = random.choice(list(neighbors.keys()))
                    if direction == "east" and neighbors["east"]:
                        self.maze.link_cells(working_cell, neighbors["east"])
                        self.visual_effects["last_linked"] = neighbors["east"]
                        working_cell = neighbors["east"]
                        self.visual_effects["working_cell"] = working_cell
                        run.append(working_cell)
                        unvisited_cells.pop(0)
                    elif direction == "north":
                        working_cell = random.choice(run)
                        self.visual_effects["working_cell"] = working_cell
                        neighbor_north = self.maze.get_neighbors(working_cell, ignore_mask=True)["north"]
                        if neighbor_north:
                            self.maze.link_cells(working_cell, neighbor_north)
                            self.visual_effects["last_linked"] = neighbor_north
                        run.clear()
                    yield self.maze
