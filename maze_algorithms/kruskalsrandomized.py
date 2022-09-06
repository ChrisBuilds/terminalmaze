from grid.grid import Grid, Cell
import random
from typing import Union


class KruskalsRandomized:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze: Grid = maze
        self.showlogic: bool = showlogic
        self.logic_data: dict[str, Cell] = {}
        self.status_text: dict[str, Union[str, int]] = {"Algorithm": "Kruskal's Randomized"}

    def generate_maze(self) -> Grid:
        group_a_logic = list()
        group_b_logic = list()
        self.logic_data["logic1"] = group_a_logic
        self.logic_data["logic0"] = group_b_logic
        links: list[tuple[Cell, Cell]] = list()
        groups = list()
        group_map = {}  # cell_address : group
        group_id = 0
        for cell in self.maze.each_cell():
            # initialize groups
            groups.append(group_id)
            group_map[(cell.row, cell.column)] = group_id
            group_id += 1
            # find all links
            for neighbor in self.maze.get_neighbors(cell).values():
                if (neighbor, cell) not in links:  # check if reversed link is already in list
                    links.append((cell, neighbor))

        while len(groups) > 1:
            link = links.pop(random.randrange(len(links)))
            cell_a = link[0]
            cell_a_address = (cell_a.row, cell_a.column)
            cell_a_group = group_map[cell_a_address]
            cell_b = link[1]
            cell_b_address = (cell_b.row, cell_b.column)
            cell_b_group = group_map[cell_b_address]
            if cell_a_group == cell_b_group:
                continue
            self.maze.link_cells(cell_a, cell_b)
            groups.remove(cell_b_group)
            for cell, group in group_map.items():
                if group == cell_a_group:
                    group_a_logic.append(self.maze.get_cell(cell))
                if group == cell_b_group:
                    group_b_logic.append(self.maze.get_cell(cell))
                    group_map[cell] = cell_a_group
                # if self.showlogic:
                #     if group in (cell_a_group, cell_b_group):
                #        if len(group_b_logic) > 20 and len(group_a_logic) > 20:
                #            yield self.maze
            group_a_logic.clear()
            group_b_logic.clear()

            self.status_text["Available Links"] = len(links)
            self.status_text["Groups"] = len(groups)
            yield self.maze
