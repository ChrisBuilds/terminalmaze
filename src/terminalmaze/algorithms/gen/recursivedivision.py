import random
from typing import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import RecursiveDivisionTheme
from terminalmaze.resources.grid import Grid


class RecursiveDivision(Algorithm):
    def __init__(self, maze: Grid, theme: RecursiveDivisionTheme) -> None:
        super().__init__(maze, theme)
        self.status_text["Algorithm"] = "Recursive Division"
        self.status_text["Divisions"] = f"{0: >4}"
        self.status_text["State"] = ""

        self.divisions = 0
        self.theme = theme
        self.skip_frames = 30
        self.ve_working_cell = ve.Animation(self.theme.working_cell)
        self.visual_effects["working_cell"] = self.ve_working_cell
        self.ve_division_cell_east = ve.Animation(self.theme.division_cell_east)
        self.visual_effects["division_cell_east"] = self.ve_division_cell_east
        self.ve_division_cell_west = ve.Animation(self.theme.division_cell_west)
        self.visual_effects["division_cell_west"] = self.ve_division_cell_west
        self.ve_division_cell_south = ve.Animation(self.theme.division_cell_south)
        self.visual_effects["division_cell_south"] = self.ve_division_cell_south
        self.ve_division_cell_north = ve.Animation(self.theme.division_cell_north)
        self.visual_effects["division_cell_north"] = self.ve_division_cell_north
        self.ve_generating_links_cells = ve.Animation(self.theme.generating_links_cells)
        self.visual_effects["generating_links_cells"] = self.ve_generating_links_cells
        self.ve_passage_cell = ve.Animation(self.theme.passage_cell)
        self.visual_effects["passage_cell"] = self.ve_passage_cell

    def generate_maze(self) -> Generator[Grid, None, None]:
        all_cells = list(self.maze.each_cell(ignore_mask=True))
        while all_cells:
            working_cell = all_cells.pop(random.randint(0, len(all_cells) - 1))
            self.ve_generating_links_cells.cells.append(working_cell)
            for _, neighbor in self.maze.get_neighbors(working_cell, ignore_mask=True).items():
                if neighbor and neighbor not in working_cell.links:
                    self.maze.link_cells(working_cell, neighbor)
                    self.ve_generating_links_cells.cells.append(neighbor)
                    if self.frame_wanted():
                        yield self.maze
        while self.ve_generating_links_cells.animating:
            yield self.maze
        for state in self.divide(
            0, 0, len(list(self.maze.each_row(ignore_mask=True))), len(list(self.maze.each_column(ignore_mask=True)))
        ):
            yield state
        self.status_text["State"] = "Complete"
        while (
            self.ve_division_cell_north.animating
            or self.ve_division_cell_east.animating
            or self.ve_division_cell_south.animating
            or self.ve_division_cell_west.animating
        ):
            yield self.maze

    def divide(self, row, column, height, width):
        if width <= 1 or height <= 1:
            return
        if width > height:
            self.divisions += 1
            self.status_text["Divisions"] = f"{self.divisions: >4}"
            for state in self.divide_vertically(row, column, height, width):
                yield state
        else:
            self.divisions += 1
            self.status_text["Divisions"] = f"{self.divisions: >4}"
            for state in self.divide_horizontally(row, column, height, width):
                yield state

    def divide_horizontally(self, row, column, height, width):
        self.status_text["State"] = "Dividing Horizontally"
        wall_row_index = random.randint(0, height - 2)
        passage_index = random.randint(0, width - 1)
        for cell_column in range(0, width):
            if cell_column == passage_index:
                self.ve_passage_cell.cells.append(self.maze.get_cell((row + wall_row_index, column + cell_column)))
                continue
            cell = self.maze.get_cell((row + wall_row_index, column + cell_column))
            neighbors = self.maze.get_neighbors(cell, ignore_mask=True)
            if "south" in neighbors and neighbors["south"] and neighbors["south"] in cell.links:
                self.maze.unlink_cells(cell, neighbors["south"])
                self.ve_working_cell.cells.append(cell)
                self.ve_division_cell_north.cells.append(cell)
                self.ve_division_cell_south.cells.append(neighbors["south"])
                yield self.maze

        if (wall_row_index + 1) * width < (height - wall_row_index - 1) * width:
            for state in self.divide(row, column, wall_row_index + 1, width):
                yield state
            for state in self.divide(row + wall_row_index + 1, column, height - wall_row_index - 1, width):
                yield state
        else:
            for state in self.divide(row + wall_row_index + 1, column, height - wall_row_index - 1, width):
                yield state
            for state in self.divide(row, column, wall_row_index + 1, width):
                yield state

    def divide_vertically(self, row, column, height, width):
        self.status_text["State"] = "Dividing Vertically"
        wall_column_index = random.randint(0, width - 2)
        passage_index = random.randint(0, height - 1)
        for cell_row in range(0, height):
            if cell_row == passage_index:
                continue
            cell = self.maze.get_cell((row + cell_row, column + wall_column_index))
            neighbors = self.maze.get_neighbors(cell, ignore_mask=True)
            if "east" in neighbors and neighbors["east"] and neighbors["east"] in cell.links:
                self.maze.unlink_cells(cell, neighbors["east"])
                self.ve_working_cell.cells.append(cell)
                self.ve_division_cell_west.cells.append(cell)
                self.ve_division_cell_east.cells.append(neighbors["east"])
                yield self.maze

        if (height * (wall_column_index + 1)) < (height * (width - wall_column_index - 1)):
            for state in self.divide(row, column, height, wall_column_index + 1):
                yield state
            for state in self.divide(row, column + wall_column_index + 1, height, width - wall_column_index - 1):
                yield state
        else:
            for state in self.divide(row, column + wall_column_index + 1, height, width - wall_column_index - 1):
                yield state
            for state in self.divide(row, column, height, wall_column_index + 1):
                yield state
