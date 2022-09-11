from terminalmaze.resources.grid import Grid
from terminalmaze.resources.cell import Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import terminalmaze.tools.visualeffects as ve

import random
from collections import defaultdict
from typing import Generator


class KruskalsRandomized(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.group_to_cell_map_logic: defaultdict[int, set[Cell]] = defaultdict(set)  # group : {cells}
        self.cell_to_group_map: dict[Cell, int] = {}  # cell_address : group
        self.status_text["Algorithm"] = "Kruskal's Randomized"

    def generate_maze(self) -> Generator[Grid, None, None]:
        links: set[tuple[Cell, Cell]] = set()
        groups = list()
        group_id = 0
        for cell in self.maze.each_cell():
            # initialize groups
            groups.append(group_id)
            self.cell_to_group_map[cell] = group_id
            # group_to_cell_map_logic[group_id].append(cell)
            group_id += 1
            # find all links
            for neighbor in self.maze.get_neighbors(cell).values():
                if (neighbor, cell) not in links and neighbor:  # check if reversed link is already in list
                    links.add((cell, neighbor))

        ve_groups = ve.RandomColorGroup(layer=0, groups=self.group_to_cell_map_logic)
        self.visual_effects["groups"] = ve_groups

        while len(groups) > 1:
            link = links.pop()
            cell_a = link[0]
            cell_a_group = self.cell_to_group_map[cell_a]
            cell_b = link[1]
            cell_b_group = self.cell_to_group_map[cell_b]
            if cell_a not in self.group_to_cell_map_logic[cell_a_group]:
                self.group_to_cell_map_logic[cell_a_group].add(cell_a)
            if cell_b not in self.group_to_cell_map_logic[cell_b_group]:
                self.group_to_cell_map_logic[cell_b_group].add(cell_b)
            if cell_a_group == cell_b_group:
                continue
            self.maze.link_cells(cell_a, cell_b)
            self.merge_groups(cell_a, cell_b, groups)

            self.status_text["Time Elapsed"] = self.time_elapsed()
            self.status_text["Available Links"] = len(links)
            self.status_text["Groups"] = len(groups)
            yield self.maze

    def merge_groups(self, cell_a: Cell, cell_b: Cell, groups):
        cell_a_group = self.cell_to_group_map[cell_a]
        cell_b_group = self.cell_to_group_map[cell_b]
        smaller_group, larger_group = sorted(
            [cell_a_group, cell_b_group], key=lambda group: len(self.group_to_cell_map_logic[group])
        )
        self.group_to_cell_map_logic[larger_group].update(self.group_to_cell_map_logic[smaller_group])
        del self.group_to_cell_map_logic[smaller_group]
        for cell, group in self.cell_to_group_map.items():
            if group == smaller_group:
                if cell_a_group == larger_group:
                    self.cell_to_group_map[cell] = cell_a_group
                elif cell_b_group == larger_group:
                    self.cell_to_group_map[cell] = cell_b_group
        groups.remove(smaller_group)
