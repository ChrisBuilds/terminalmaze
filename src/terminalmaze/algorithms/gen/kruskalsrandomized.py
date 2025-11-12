import random
from collections import defaultdict
from typing import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import KruskalsRandomizedTheme
from terminalmaze.resources.cell import Cell
from terminalmaze.resources.grid import Grid


class KruskalsRandomized(Algorithm):
    def __init__(self, maze: Grid, theme: KruskalsRandomizedTheme) -> None:
        super().__init__(maze, theme)
        self.theme = theme
        self.group_to_cell_map_logic: defaultdict[int, set[Cell]] = defaultdict(set)  # group : {cells}
        self.cell_to_group_map: dict[Cell, int] = dict()  # cell_address : group
        self.status_text["Algorithm"] = "Kruskal's Randomized"
        self.status_text["Available Links"] = 0
        self.status_text["Groups"] = 0
        self.status_text["State"] = ""

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

        ve_groups = ve.RandomColorGroup(self.theme.group_random_color)
        ve_groups.groups = self.group_to_cell_map_logic
        self.visual_effects["groups"] = ve_groups

        while len(groups) > 1:
            self.status_text["State"] = "Merging Groups"
            link = random.choice(list(links))
            links.discard(link)
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

            self.status_text["Available Links"] = len(links)
            self.status_text["Groups"] = len(groups)
            yield self.maze
        self.status_text["State"] = "Complete"
        yield self.maze

    def merge_groups(self, cell_a: Cell, cell_b: Cell, groups):
        cell_a_group = self.cell_to_group_map[cell_a]
        cell_b_group = self.cell_to_group_map[cell_b]
        smaller_group, larger_group = sorted(
            [cell_a_group, cell_b_group], key=lambda cell_group: len(self.group_to_cell_map_logic[cell_group])
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
