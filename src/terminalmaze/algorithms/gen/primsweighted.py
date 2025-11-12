import random
from typing import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import PrimsWeightedTheme
from terminalmaze.resources.grid import Cell, Grid


class PrimsWeighted(Algorithm):
    def __init__(self, maze: Grid, theme: PrimsWeightedTheme) -> None:
        super().__init__(maze, theme)
        self.theme = theme
        self.status_text["Algorithm"] = "Prims Weighted"
        self.status_text["Edges"] = 0
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""

    def generate_maze(self) -> Generator[Grid, None, None]:
        ve_working_cell = ve.Animation(self.theme.working_cell)
        self.visual_effects["working_cell"] = ve_working_cell

        ve_unlinked_neighbors = ve.Animation(self.theme.unlinked_neighbors)
        self.visual_effects["unlinkedneighbors"] = ve_unlinked_neighbors

        ve_last_linked = ve.Animation(self.theme.last_linked)
        self.visual_effects["last_linked"] = ve_last_linked

        ve_pending_weighted_links = ve.ModifyMultipleCells(self.theme.pending_weighted_links)
        self.visual_effects["pending_weighted_links"] = ve_pending_weighted_links

        ve_new_weighted_links = ve.Animation(self.theme.new_weighted_links)
        self.visual_effects["new_weighted_links"] = ve_new_weighted_links

        total_cells_unlinked = 0
        cell_weights = {}
        for cell in self.maze.each_cell():
            cell_weights[cell] = random.randint(0, 99)
            total_cells_unlinked += 1
        cell = self.maze.random_cell()
        pending_weighted_links = list()
        unlinked_neighbors = list(n for n in self.maze.get_neighbors(cell).values() if n and not n.links)
        for neighbor in unlinked_neighbors:
            pending_weighted_links.append((cell, neighbor, cell_weights[neighbor]))
        while pending_weighted_links:
            self.status_text["State"] = "Linking"
            ve_pending_weighted_links.cells = [link[0] for link in pending_weighted_links]
            next_cell: Cell
            working_cell: Cell

            working_cell, next_cell, cost = min(pending_weighted_links, key=lambda link: link[2])
            ve_working_cell.cells.append(working_cell)
            pending_weighted_links.remove((working_cell, next_cell, cost))
            if next_cell.links:
                continue
            self.maze.link_cells(working_cell, next_cell)
            total_cells_unlinked -= 1
            ve_last_linked.cells.append(next_cell)
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
            ve_unlinked_neighbors.cells.extend(unlinked_neighbors)
            if unlinked_neighbors:
                for neighbor in unlinked_neighbors:
                    pending_weighted_links.append((next_cell, neighbor, cell_weights[neighbor]))
                    ve_new_weighted_links.cells.append(next_cell)
            self.status_text["Edges"] = len(pending_weighted_links)
            self.status_text["Unlinked Cells"] = total_cells_unlinked
            yield self.maze

        while (
            ve_last_linked.animating
            or ve_unlinked_neighbors.animating
            or ve_working_cell.animating
            or ve_new_weighted_links.animating
        ):
            yield self.maze

        self.visual_effects.clear()
        total_cells_unlinked -= 1
        self.status_text["Edges"] = 0
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = "Complete"
        yield self.maze
