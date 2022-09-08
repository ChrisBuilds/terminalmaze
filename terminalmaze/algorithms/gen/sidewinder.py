from operator import ne
import random
from collections.abc import Generator

from resources.grid import Grid
from resources.cell import Cell


class Sidewinder:
    def __init__(self, maze: Grid, showlogic: bool = False):
        """
        For each row, randomly link cells in a run of cells to their north or east neighbor.
        """
        self.maze = maze
        self.showlogic = showlogic
        self.logic_data = {}
        self.status_text = {"Algorithm": "Sidewinder", "Seed": self.maze.seed}
        random.seed(self.maze.seed)

    def generate_maze(self) -> Generator[Grid, None, None]:
        run: list[Cell] = []
        self.logic_data["logic0"] = run
        for row in self.maze.each_row(ignore_mask=True, bottom_up=True):
            unvisited_cells = row.copy()
            while unvisited_cells:
                working_cell = unvisited_cells.pop(0)
                self.logic_data["working_cell"] = working_cell
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
                    if direction == "east":
                        self.maze.link_cells(working_cell, neighbors["east"])
                        self.logic_data["last_linked"] = neighbors["east"]
                        working_cell = neighbors["east"]
                        self.logic_data["working_cell"] = working_cell
                        run.append(working_cell)
                        unvisited_cells.pop(0)
                    elif direction == "north":
                        working_cell = random.choice(run)
                        self.logic_data["working_cell"] = working_cell
                        self.maze.link_cells(
                            working_cell, self.maze.get_neighbors(working_cell, ignore_mask=True)["north"]
                        )
                        self.logic_data["last_linked"] = working_cell.neighbors["north"]
                        run.clear()
                    yield self.maze
