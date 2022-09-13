from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
import random
from typing import Generator


class RecursiveBacktracker(Algorithm):
    def __init__(self, maze: Grid) -> None:
        super().__init__(maze)
        self.status_text["Algorithm"] = "Recursive Backtracker"
        self.status_text.update({"Pending Paths": "", "Stack Length": "", "State": ""})
        self.skip_frames = 2

    def generate_maze(self) -> Generator[Grid, None, None]:
        cell = self.maze.random_cell()
        stack = [cell]
        backtracked: list[Cell] = list()
        stacktrail: list[Cell] = list()
        ve_stack = ve.ColorMultipleCells(layer=0, category=ve.STYLE, color=218, cells=stack)
        self.visual_effects["stack"] = ve_stack
        ve_workingcell = ve.ColorSingleCell(layer=1, category=ve.LOGIC, color=218, cell=cell)
        self.visual_effects["working_cell"] = ve_workingcell
        ve_invalidneighbors = ve.ColorMultipleCells(layer=1, category=ve.LOGIC, color=52, cells=[])
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors
        ve_lastlinked = ve.ColorSingleCell(layer=1, category=ve.LOGIC, color=218, cell=cell)
        self.visual_effects["last_linked"] = ve_lastlinked
        ve_stacktrail = ve.TrailingColor(
            layer=1,
            category=ve.STYLE,
            colors=[200, 200, 201, 201, 204, 204, 205, 205, 205, 206, 206, 207, 207],
            cells=stacktrail,
        )
        self.visual_effects["stack_trail"] = ve_stacktrail
        ve_backtracktrail = ve.TrailingColor(
            layer=2, category=ve.STYLE, colors=[224, 224, 188, 188, 158, 158, 159, 159, 86, 86, 44, 44, 6], cells=[]
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

        self.visual_effects.clear()
        yield self.maze
