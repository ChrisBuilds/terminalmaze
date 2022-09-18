from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
import random
from typing import Generator


class PrimsWeighted(Algorithm):
    def __init__(self, maze: Grid, theme: ve.Theme) -> None:
        super().__init__(maze)
        self.theme = theme["prims_weighted"]
        self.status_text["Algorithm"] = "Prims Weighted"
        self.status_text["Edges"] = 0
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = ""

    def generate_maze(self) -> Generator[Grid, None, None]:
        lastlinked: list[Cell] = []
        ve_lastlinked = ve.ColorTrail(
            layer=1,
            category=ve.STYLE,
            cells=lastlinked,
            colors=self.theme["lastlinked"],  # type: ignore [arg-type]
            traveldir=0,
        )
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_links = ve.ColorMultipleCells(
            layer=0, category=ve.STYLE, cells=[], color=self.theme["links"]  # type: ignore [arg-type]
        )
        self.visual_effects["links"] = ve_links
        ve_workingcell = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, cell=Cell(0, 0), color=self.theme["workingcell"]  # type: ignore [arg-type]
        )
        self.visual_effects["working_cell"] = ve_workingcell
        ve_unlinkedneighbors = ve.ColorMultipleCells(
            layer=0, category=ve.LOGIC, cells=[], color=self.theme["unlinkedneighbors"]  # type: ignore [arg-type]
        )
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
            lastlinked.insert(0, next_cell)
            if len(lastlinked) == 10:
                lastlinked.pop()
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
            ve_unlinkedneighbors.cells = unlinked_neighbors
            if unlinked_neighbors:
                for neighbor in unlinked_neighbors:
                    links.append((next_cell, neighbor, cell_weights[neighbor]))
            self.status_text["Edges"] = len(links)
            self.status_text["Unlinked Cells"] = total_cells_unlinked
            yield self.maze

        self.visual_effects.clear()
        total_cells_unlinked -= 1
        self.status_text["Edges"] = 0
        self.status_text["Unlinked Cells"] = 0
        self.status_text["State"] = "Complete"
        yield self.maze
