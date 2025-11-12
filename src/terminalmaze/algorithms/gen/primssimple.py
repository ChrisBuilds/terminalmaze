import random
from typing import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import PrimsSimpleTheme
from terminalmaze.resources.grid import Grid


class PrimsSimple(Algorithm):
    def __init__(self, maze: Grid, theme: PrimsSimpleTheme) -> None:
        super().__init__(maze, theme)
        self.theme = theme
        self.status_text["Algorithm"] = "Prims Simplified"
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""
        self.edge_frame_ratio = self.theme.edge_frame_ratio

    def generate_maze(self) -> Generator[Grid, None, None]:
        total_unlinked_cells = len(list(self.maze.each_cell()))
        self.status_text["Unlinked Cells"] = total_unlinked_cells
        cell = self.maze.random_cell()
        edge_cells = list()
        edge_cells.append(cell)

        ve_edges = ve.Animation(self.theme.edges)
        ve_edges.cells.append(cell)
        self.visual_effects["edges"] = ve_edges

        ve_workingcell = ve.Animation(self.theme.working_cell)
        ve_workingcell.cells.append(cell)
        self.visual_effects["working_cell"] = ve_workingcell

        ve_invalidneighbors = ve.Animation(self.theme.invalid_neighbors)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors

        ve_lastlinked = ve.Animation(self.theme.last_linked)
        ve_lastlinked.cells.append(cell)
        self.visual_effects["last_linked"] = ve_lastlinked

        while edge_cells:
            self.status_text["State"] = "Linking"
            working_cell = edge_cells.pop(random.randrange(len(edge_cells)))
            ve_workingcell.cells.append(working_cell)
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(working_cell).values() if neighbor]
            unlinked_neighbors = [neighbor for neighbor in neighbors if not neighbor.links]
            ve_invalidneighbors.cells.extend([neighbor for neighbor in neighbors if neighbor.links])
            if unlinked_neighbors:
                next_cell = unlinked_neighbors.pop(random.randrange(len(unlinked_neighbors)))
                self.maze.link_cells(working_cell, next_cell)
                total_unlinked_cells -= 1
                self.status_text["Unlinked Cells"] = total_unlinked_cells
                ve_lastlinked.cells.append(next_cell)
                if unlinked_neighbors:
                    edge_cells.append(working_cell)
                    ve_edges.cells.append(working_cell)
                unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
                if unlinked_neighbors:
                    edge_cells.append(next_cell)
                    ve_edges.cells.append(working_cell)
            if self.frame_wanted_relative(edge_cells, divisor=self.edge_frame_ratio):
                yield self.maze
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State:"] = "Complete"
        while (
            ve_edges.animating or ve_workingcell.animating or ve_lastlinked.animating or ve_invalidneighbors.animating
        ):
            yield self.maze
        yield self.maze
