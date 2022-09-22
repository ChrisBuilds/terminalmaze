from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from terminalmaze.config import PrimsSimpleTheme
import random
from typing import Generator


class PrimsSimple(Algorithm):
    def __init__(self, maze: Grid, theme: PrimsSimpleTheme) -> None:
        super().__init__(maze)
        self.theme = theme
        self.status_text["Algorithm"] = "Prims Simplified"
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""
        self.skip_frames = 0

    def generate_maze(self) -> Generator[Grid, None, None]:
        total_unlinked_cells = len(list(self.maze.each_cell()))
        self.status_text["Unlinked Cells"] = total_unlinked_cells
        cell = self.maze.random_cell()
        edge_cells = list()
        edge_cells.append(cell)
        ve_edges = ve.ColorMultipleCells(self.theme.edges)
        ve_edges.cells = edge_cells
        self.visual_effects["edges"] = ve_edges
        ve_workingcell = ve.ColorSingleCell(self.theme.working_cell)
        ve_workingcell.cell = cell
        self.visual_effects["working_cell"] = ve_workingcell
        ve_invalidneighbors = ve.ColorMultipleCells(self.theme.invalid_neighbors)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_lastlinked = ve.ColorSingleCell(self.theme.last_linked)
        ve_lastlinked.cell = cell
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_oldedges = ve.ColorMultipleCells(self.theme.old_edges)
        self.visual_effects["old_edges"] = ve_oldedges

        while edge_cells:
            self.status_text["State"] = "Linking"
            working_cell = edge_cells.pop(random.randrange(len(edge_cells)))
            ve_oldedges.cells.append(working_cell)
            ve_oldedges.cells = ve_oldedges.cells[-len(edge_cells) :]
            ve_workingcell.cell = working_cell
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(working_cell).values() if neighbor]
            unlinked_neighbors = [neighbor for neighbor in neighbors if not neighbor.links]
            ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if neighbor.links]
            if unlinked_neighbors:
                next_cell = unlinked_neighbors.pop(random.randrange(len(unlinked_neighbors)))
                self.maze.link_cells(working_cell, next_cell)
                total_unlinked_cells -= 1
                self.status_text["Unlinked Cells"] = total_unlinked_cells
                ve_lastlinked.cell = next_cell
                if unlinked_neighbors:
                    edge_cells.append(working_cell)
                unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
                if unlinked_neighbors:
                    edge_cells.append(next_cell)
            if self.frame_wanted_relative(edge_cells, divisor=10):
                yield self.maze
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State:"] = "Complete"
        self.visual_effects.clear()
        yield self.maze
