import random
from collections import defaultdict
from typing import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import EllersTheme
from terminalmaze.resources.cell import Cell
from terminalmaze.resources.grid import Grid


class Ellers(Algorithm):
    def __init__(self, maze: Grid, theme: EllersTheme) -> None:
        super().__init__(maze, theme)
        self.ignore_mask = True
        self.theme = theme
        self.status_text["Algorithm"] = "Eller's"
        self.status_text["Seed"] = self.maze.seed
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""

    def generate_maze(self) -> Generator[Grid, None, None]:
        unlinked_cells = set(self.maze.each_cell())
        cell_to_group: dict[tuple[int, int], int] = {}  # cell_address : group
        group_to_cell: defaultdict[int, list[Cell]] = defaultdict(list)  # group : Cell
        ve_groups = ve.RandomColorGroup(self.theme.group_to_random_color)
        ve_groups.groups = group_to_cell
        self.visual_effects["groups"] = ve_groups
        group_id = 0
        for i, row in enumerate(self.maze.each_row(ignore_mask=self.ignore_mask)):
            row_groups: defaultdict[int, list[Cell]] = defaultdict(list)
            for cell in row:
                cell_address = (cell.row, cell.column)
                if cell_address not in cell_to_group:
                    cell_to_group[cell_address] = group_id
                    group_to_cell[group_id].append(cell)
                    row_groups[group_id].append(cell)
                    group_id += 1
                else:
                    row_groups[cell_to_group[cell_address]].append(cell)
            if i == self.maze.height - 1:
                links_to_make = len(row_groups) - 1
            else:
                group_count = len(row_groups)
                if group_count > 1:
                    links_to_make = random.randint(0, group_count - 1)
                else:
                    links_to_make = 0
            unchecked_cells = [cell for cell in row]
            while links_to_make:
                self.status_text["State"] = "Merging Groups"
                cell = random.choice(unchecked_cells)
                cell_address = (cell.row, cell.column)
                cell_group = cell_to_group[cell_address]
                for direction, neighbor in self.maze.get_neighbors(cell, ignore_mask=self.ignore_mask).items():
                    if direction not in ("east", "west") or not neighbor:
                        continue
                    neighbor_address = (neighbor.row, neighbor.column)
                    neighbor_group = cell_to_group[neighbor_address]
                    if cell in neighbor.links or cell_group == neighbor_group:
                        continue
                    self.maze.link_cells(cell, neighbor)
                    unlinked_cells.discard(cell)
                    unlinked_cells.discard(neighbor)
                    self.status_text["Unlinked Cells"] = len(unlinked_cells)
                    cell_to_group[neighbor_address] = cell_group
                    for group_member in [member for member in row_groups[neighbor_group]]:
                        row_groups[neighbor_group].remove(group_member)
                        row_groups[cell_group].append(group_member)
                        cell_to_group[(group_member.row, group_member.column)] = cell_group
                    group_to_cell[cell_group].extend(group_to_cell[neighbor_group])
                    del group_to_cell[neighbor_group]
                    if not row_groups[neighbor_group]:
                        del row_groups[neighbor_group]
                    links_to_make -= 1
                    yield self.maze
                    break
            if i == self.maze.height - 1:
                break
            for group, group_cells in row_groups.items():
                group_cells = [cell for cell in group_cells]
                cell_count = len(group_cells)
                cells_to_drop = random.randint(1, cell_count)
                while cells_to_drop:
                    self.status_text["State"] = "Dropping"
                    cell = group_cells.pop(random.randint(0, len(group_cells) - 1))
                    neighbor = self.maze.get_neighbors(cell, ignore_mask=self.ignore_mask)["south"]
                    if not neighbor:
                        continue
                    neighbor_address = (neighbor.row, neighbor.column)
                    cell_to_group[neighbor_address] = group
                    group_to_cell[cell_to_group[(cell.row, cell.column)]].append(neighbor)
                    cells_to_drop -= 1
                    self.maze.link_cells(cell, neighbor)
                    unlinked_cells.discard(cell)
                    unlinked_cells.discard(neighbor)
                    self.status_text["Unlinked Cells"] = len(unlinked_cells)
                    yield self.maze

        self.status_text["State"] = "Complete"
        yield self.maze
