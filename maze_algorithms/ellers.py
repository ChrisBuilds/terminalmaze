from tokenize import group
from grid.grid import Grid, Cell
import random
from collections import defaultdict
from typing import Union


class Ellers:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.mask_incompatible = True
        self.logic_data: dict[str, Cell] = {}
        self.status_text: dict[str, Union[str, int]] = {"Algorithm": "Eller's"}

    def generate_maze(self) -> Grid:
        cell_to_group: dict[tuple[int, int], int] = {}  # cell_address : group
        group_to_cell: defaultdict[int, list[Cell]] = defaultdict(list)  # group : Cell
        group_id = 0
        for i, row in enumerate(self.maze.each_row(ignore_mask=self.mask_incompatible)):
            row_groups: defaultdict[int, list[Cell]] = defaultdict(list)
            for cell in row:
                cell_address = (cell.row, cell.column)
                if cell_address not in cell_to_group:
                    # initialize groups
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
                cell = random.choice(unchecked_cells)
                cell_address = (cell.row, cell.column)
                cell_group = cell_to_group[cell_address]
                for direction, neighbor in self.maze.get_neighbors(cell, ignore_mask=self.mask_incompatible).items():
                    if direction not in ("east", "west"):
                        continue
                    neighbor_address = (neighbor.row, neighbor.column)
                    neighbor_group = cell_to_group[neighbor_address]
                    if cell in neighbor.links or cell_group == neighbor_group:
                        continue
                    self.maze.link_cells(cell, neighbor)
                    cell_to_group[neighbor_address] = cell_group
                    for group_member in [
                        member for member in row_groups[neighbor_group]
                    ]:  # fix modifying list during iteration
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
                    cell = group_cells.pop(random.randint(0, len(group_cells) - 1))
                    neighbor = self.maze.get_neighbors(cell, ignore_mask=self.mask_incompatible)["south"]
                    neighbor_address = (neighbor.row, neighbor.column)
                    self.maze.link_cells(cell, neighbor)
                    cell_to_group[neighbor_address] = group
                    cells_to_drop -= 1
        yield self.maze
