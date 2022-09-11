from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
import terminalmaze.tools.visualeffects as ve
import random
from typing import Generator


class PrimsWeighted(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Prims Weighted"
        self.status_text["Seed"] = self.maze.seed

    def generate_maze(self) -> Generator[Grid, None, None]:
        last_linked: list[Cell] = []
        ve_lastlinked = ve.ColorMultipleCells(layer=0, cells=last_linked, color=49)
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_links = ve.ColorMultipleCells(layer=0, cells=[], color=14)
        self.visual_effects["links"] = ve_links

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
            ve_links.cells = [link[0] for link in links]
            next_cell: Cell
            working_cell: Cell

            working_cell, next_cell, cost = min(links, key=lambda link: link[2])
            links.remove((working_cell, next_cell, cost))
            if next_cell.links:
                continue
            self.maze.link_cells(working_cell, next_cell)
            total_cells_unlinked -= 1
            last_linked.append(next_cell)
            if len(last_linked) == 10:
                last_linked.pop(0)
            unlinked_neighbors = list(n for n in self.maze.get_neighbors(next_cell).values() if n and not n.links)
            if unlinked_neighbors:
                for neighbor in unlinked_neighbors:
                    links.append((next_cell, neighbor, cell_weights[neighbor]))
            self.status_text["Time Elapsed"] = self.time_elapsed()
            self.status_text["Edges"] = len(links)
            self.status_text["Unlinked Cells"] = total_cells_unlinked
            yield self.maze

        self.visual_effects = {}
        total_cells_unlinked -= 1
        self.status_text["Edges"] = 0
        yield self.maze
