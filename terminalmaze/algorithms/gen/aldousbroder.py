from terminalmaze.algorithms.gen.mazealgorithm import MazeAlgorithm
from terminalmaze.resources.grid import Grid, Cell
import terminalmaze.tools.visualeffects as ve
import random
import time
from collections.abc import Generator


class AldousBroder(MazeAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text = {
            "Algorithm": "Aldous Broder",
            "Seed": self.maze.seed,
            "Time Elapsed": "",
            "Unvisited": "",
            "Revisited": "",
            "Cell": "",
        }
        self.frame_time = time.time()

    def generate_maze(self) -> Generator[Grid, None, None]:
        unvisited = set(self.maze.each_cell())
        working_cell = unvisited.pop()
        self.last_linked: list[Cell] = list()
        self.invalid_visited: list[Cell] = list()
        ve_workingcell = ve.ColorSingleCell(layer=0, cell=working_cell, color=218)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_lastlinked = ve.ColorMultipleCells(layer=0, cells=self.last_linked, color=218)
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_invalidneighbors = ve.ColorMultipleCells(layer=1, cells=[], color=159)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_invalidvisited = ve.ColorMultipleCells(layer=0, cells=self.invalid_visited, color=159)
        self.visual_effects["invalid_visited"] = ve_invalidvisited
        waste = 0
        while unvisited:
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(working_cell).values() if neighbor]
            ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if neighbor not in unvisited]
            neighbor = random.choice(neighbors)
            if neighbor in unvisited:
                self.maze.link_cells(working_cell, neighbor)
                self.last_linked.append(neighbor)
                if len(self.last_linked) == 10:
                    self.last_linked.pop(0)
                unvisited.discard(neighbor)
                self.status_text["Unvisited"] = len(unvisited)
                self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                self.status_text["Time Elapsed"] = self.time_elapsed()
                yield self.maze
            else:
                waste += 1
                self.status_text["Revisited"] = waste
                time_since_last_frame = time.time() - self.frame_time
                if time_since_last_frame > 0.15:
                    self.frame_time = time.time()
                    self.status_text["Unvisited"] = len(unvisited)
                    self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                    self.status_text["Time Elapsed"] = self.time_elapsed()
                    ve_invalidvisited.cells.append(neighbor)
                    ve_invalidvisited.cells = ve_invalidvisited.cells[-25:]
                    yield self.maze

            working_cell = neighbor
            ve_workingcell.cell = working_cell

        yield self.maze
