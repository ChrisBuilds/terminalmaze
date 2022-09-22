from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from terminalmaze.config import PrimsWeightedTheme
import random
from typing import Generator


class PrimsWeighted(Algorithm):
    def __init__(self, maze: Grid, theme: PrimsWeightedTheme) -> None:
        super().__init__(maze)
        self.theme = theme
        self.status_text["Algorithm"] = "Prims Weighted"
        self.status_text["Edges"] = 0
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""

    def generate_maze(self) -> Generator[Grid, None, None]:
        ve_lastlinked = ve.ValueTransition(self.theme.last_linked_transition)
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_links = ve.ColorMultipleCells(self.theme.links)
        self.visual_effects["links"] = ve_links
        ve_workingcell = ve.ColorSingleCell(self.theme.working_cell)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_unlinkedneighbors = ve.ColorMultipleCells(self.theme.unlinked_neighbors)
        self.visual_effects["unlinkedneighbors"] = ve_unlinkedneighbors

        total_cells_unlinked = 0
        cell_weights = {}
        for cell in self.maze.each_cell():
            cell_weights[cell] = random.randint(0, 99)
            total_cells_unlinked += 1
        cell = self.maze.random_cell()
        links = list()
        unlinked_neighbors = list(n for n in self.maze.get_neighbors(cell).values() if n and not n.links)
        for neighbor in unlinked_neighbors:
            links.append((cell, neighbor, cell_weights[neighbor]))
        while links:
            self.status_text["State"] = "Linking"
            ve_links.cells = [link[0] for link in links]
            next_cell: Cell
            working_cell: Cell

            working_cell, next_cell, cost = min(links, key=lambda link: link[2])
            ve_workingcell.cell = working_cell
            links.remove((working_cell, next_cell, cost))
            if next_cell.links:
                continue
            self.maze.link_cells(working_cell, next_cell)
            total_cells_unlinked -= 1
            ve_lastlinked.cells.append(next_cell)
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
            ve_unlinkedneighbors.cells = unlinked_neighbors
            if unlinked_neighbors:
                for neighbor in unlinked_neighbors:
                    links.append((next_cell, neighbor, cell_weights[neighbor]))
            self.status_text["Edges"] = len(links)
            self.status_text["Unlinked Cells"] = total_cells_unlinked
            yield self.maze

        while ve_lastlinked.transitioning:
            yield self.maze

        self.visual_effects.clear()
        total_cells_unlinked -= 1
        self.status_text["Edges"] = 0
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = "Complete"
        yield self.maze
