from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.resources.grid import Grid, Cell
import terminalmaze.tools.visualeffects as ve
import random
import time
from collections.abc import Generator


class AldousBroder(Algorithm):
    def __init__(self, maze: Grid, theme: ve.Theme) -> None:
        super().__init__(maze)
        self.status_text["Algorithm"] = "Aldous Broder"
        self.status_text.update({"Unvisited": 0, "Revisited": 0, "Cell": "", "State": ""})
        self.frame_time = time.time()
        self.invalid_visited: list[Cell] = list()
        self.last_linked: list[Cell] = list()
        self.theme = theme["aldous_broder"]

    def generate_maze(self) -> Generator[Grid, None, None]:
        unvisited = set(self.maze.each_cell())
        working_cell = unvisited.pop()
        ve_workingcell = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, cell=working_cell, color=self.theme["workingcell"]  # type: ignore [arg-type]
        )
        self.visual_effects["working_cell"] = ve_workingcell
        ve_lastlinked = ve.ColorMultipleCells(
            layer=1,
            category=ve.STYLE,
            cells=self.last_linked,
            color=self.theme["lastlinked"],  # type: ignore [arg-type]
        )
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_invalidneighbors = ve.ColorMultipleCells(
            layer=0, category=ve.LOGIC, cells=[], color=self.theme["invalidneighbors"]  # type: ignore [arg-type]
        )
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_invalidvisited = ve.ColorMultipleCells(
            layer=0,
            category=ve.STYLE,
            cells=self.invalid_visited,
            color=self.theme["invalidvisited"],  # type: ignore [arg-type]
        )
        self.visual_effects["invalid_visited"] = ve_invalidvisited
        revisited = 0
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
                if ve_invalidvisited.cells:
                    ve_invalidvisited.cells.pop(0)
                self.status_text["Unvisited"] = len(unvisited)
                self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                self.status_text["Time Elapsed"] = self.time_elapsed()
                self.status_text["State"] = "Linking"
                yield self.maze
            else:
                revisited += 1
                self.status_text["Revisited"] = revisited
                self.status_text["State"] = "Searching"
                if neighbor not in ve_invalidvisited.cells:
                    ve_invalidvisited.cells.append(neighbor)
                ve_invalidvisited.cells = ve_invalidvisited.cells[-50:]
                time_since_last_frame = time.time() - self.frame_time
                if time_since_last_frame > 0.0270:
                    self.frame_time = time.time()
                    self.status_text["Unvisited"] = len(unvisited)
                    self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                    self.status_text["Time Elapsed"] = self.time_elapsed()

                    if self.last_linked:
                        self.last_linked.pop(0)
                    yield self.maze

            working_cell = neighbor
            ve_workingcell.cell = working_cell
        del self.visual_effects["working_cell"]
        del self.visual_effects["invalid_neighbors"]
        while ve_invalidvisited.cells or ve_lastlinked.cells:
            if ve_invalidvisited.cells:
                ve_invalidvisited.cells.pop(0)
            if ve_lastlinked.cells:
                ve_lastlinked.cells.pop(0)
            self.status_text["Time Elapsed"] = self.time_elapsed()
            yield self.maze
        self.status_text["State"] = "Complete"
        yield self.maze
