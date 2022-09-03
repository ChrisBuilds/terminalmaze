from operator import ne
import random
from collections.abc import Generator

from grid.grid import Grid, Cell


class Sidewinder:
    def __init__(self, grid: Grid, showlogic: bool = False):
        """
        For each row, randomly link cells in a run of cells to their north or east neighbor.
        """
        self.grid = grid
        self.showlogic = showlogic
        self.logic_data = {}

    def generate_maze(self) -> Generator[Grid, None, None]:
        run: list[Cell] = []
        self.logic_data["logic0"] = run
        for row in self.grid.each_row(bottom_up=True):
            unvisited_cells = row.copy()
            while unvisited_cells:
                working_cell = unvisited_cells.pop(0)
                self.logic_data["working_cell"] = working_cell
                run.append(working_cell)
                while run:
                    neighbors = {}
                    if working_cell.neighbors.get("north"):
                        neighbors["north"] = working_cell.neighbors["north"]
                    if working_cell.neighbors.get("east"):
                        neighbors["east"] = working_cell.neighbors["east"]
                    if not neighbors:
                        break
                    direction = random.choice(list(neighbors.keys()))
                    if direction == "east":
                        working_cell.link(neighbors["east"])
                        self.logic_data["last_linked"] = neighbors["east"]
                        working_cell = neighbors["east"]
                        self.logic_data["working_cell"] = working_cell
                        run.append(working_cell)
                        unvisited_cells.pop(0)
                    elif direction == "north":
                        working_cell = random.choice(run)
                        self.logic_data["working_cell"] = working_cell
                        working_cell.link(working_cell.neighbors["north"])
                        self.logic_data["last_linked"] = working_cell.neighbors["north"]
                        run.clear()
                    yield self.grid
