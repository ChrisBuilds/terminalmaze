from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
import random
from typing import Generator


class RecursiveBacktracker(Algorithm):
    def __init__(self, maze: Grid, theme: ve.Theme) -> None:
        super().__init__(maze)
        self.status_text["Algorithm"] = "Recursive Backtracker"
        self.status_text.update({"Pending Paths": "", "Stack Length": "", "State": ""})
        self.skip_frames = 1
        self.theme = theme["recursive_backtracker"]

    def generate_maze(self) -> Generator[Grid, None, None]:
        cell = self.maze.random_cell()
        stack = [cell]
        backtracked: list[Cell] = list()
        stacktrail: list[Cell] = list()
        ve_stack = ve.ColorMultipleCells(
            layer=0, category=ve.STYLE, color=self.theme["stack"], cells=stack  # type: ignore [arg-type]
        )
        self.visual_effects["stack"] = ve_stack
        ve_workingcell = ve.ColorSingleCell(
            layer=1, category=ve.LOGIC, color=self.theme["workingcell"], cell=cell  # type: ignore [arg-type]
        )
        self.visual_effects["working_cell"] = ve_workingcell
        ve_invalidneighbors = ve.ColorMultipleCells(
            layer=1, category=ve.LOGIC, color=self.theme["invalidneighbors"], cells=[]  # type: ignore [arg-type]
        )
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_lastlinked = ve.ColorSingleCell(
            layer=1, category=ve.LOGIC, color=self.theme["lastlinked"], cell=cell  # type: ignore [arg-type]
        )
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_stacktrail = ve.TrailingColor(
            layer=1,
            category=ve.STYLE,
            colors=self.theme["stacktrail"],  # type: ignore [arg-type]
            cells=stacktrail,
            traveldir=0,
        )
        self.visual_effects["stack_trail"] = ve_stacktrail
        ve_backtracktrail = ve.TrailingColor(
            layer=2,
            category=ve.STYLE,
            colors=self.theme["backtracktrail"],  # type: ignore [arg-type]
            cells=[],
            traveldir=0,
        )
        self.visual_effects["backtrack_trail"] = ve_backtracktrail
        while stack:
            ve_workingcell.cell = cell
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
            unvisited_neighbors = [neighbor for neighbor in neighbors if not neighbor.links]
            ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if neighbor.links]
            if unvisited_neighbors:
                if ve_backtracktrail.cells:
                    ve_backtracktrail.cells.pop(-1)
                next_cell = random.choice(unvisited_neighbors)
                self.status_text["State"] = "Walking"
                self.maze.link_cells(cell, next_cell)
                ve_stacktrail.cells.insert(0, next_cell)
                ve_stacktrail.cells = ve_stacktrail.cells[: len(ve_stacktrail.colors)]
                # ve_lastlinked.cell = next_cell
                stack.append(next_cell)
                cell = next_cell
                self.status_text["Pending Paths"] = len(unvisited_neighbors)
                self.status_text["Stack Length"] = len(stack)
                self.status_text["Time Elapsed"] = self.time_elapsed()
                yield self.maze

            else:
                if ve_stacktrail.cells:
                    ve_stacktrail.cells.pop(-1)
                ve_backtracktrail.cells.insert(0, stack.pop())
                if ve_backtracktrail.cells[0] in ve_stacktrail.cells:
                    ve_stacktrail.cells.remove(ve_backtracktrail.cells[0])
                ve_backtracktrail.cells = ve_backtracktrail.cells[: len(ve_backtracktrail.colors)]
                if stack:
                    self.status_text["State"] = "Backtracking"
                    cell = stack[-1]
                    ve_workingcell.cell = cell
                    self.status_text["Stack Length"] = len(stack)
                    if self.frame_wanted():
                        self.status_text["Time Elapsed"] = self.time_elapsed()
                        yield self.maze
        self.status_text["Stack Length"] = 0
        self.status_text["Pending Paths"] = 0
        self.status_text["State"] = "Complete"
        self.visual_effects.clear()
        yield self.maze
