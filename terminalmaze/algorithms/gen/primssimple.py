from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import terminalmaze.tools.visualeffects as ve
import random
from typing import Generator


class PrimsSimple(MazeAlgorithm):
    def __init__(self, maze: Grid) -> None:
        super().__init__(maze)
        self.status_text["Algorithm"] = "Prims Simplified"

    def generate_maze(self) -> Generator[Grid, None, None]:
        total_unlinked_cells = len(list(self.maze.each_cell()))
        self.status_text["Unlinked Cells"] = total_unlinked_cells
        cell = self.maze.random_cell()
        edge_cells = list()
        edge_cells.append(cell)
        ve_edges = ve.ColorMultipleCells(layer=0, category=ve.STYLE, cells=edge_cells, color=159)
        self.visual_effects["edges"] = ve_edges
        ve_workingcell = ve.ColorSingleCell(layer=0, category=ve.LOGIC, cell=cell, color=218)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_invalidneighbors = ve.ColorMultipleCells(layer=0, category=ve.LOGIC, cells=[], color=52)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_lastlinked = ve.ColorSingleCell(layer=0, category=ve.LOGIC, cell=cell, color=159)
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_oldedges = ve.ColorMultipleCells(layer=0, category=ve.STYLE, cells=[], color=218)
        self.visual_effects["old_edges"] = ve_oldedges

        while edge_cells:
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
            self.status_text["Time Elapsed"] = self.time_elapsed()
            yield self.maze
        self.status_text["Unlinked Cells"] = 0
        self.visual_effects.clear()
        yield self.maze
