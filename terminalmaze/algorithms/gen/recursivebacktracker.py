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

        ve_stacktrans = ve.ColorTransition(
            layer=0,
            category=ve.STYLE,
            cells=[],
            transitioning=dict(),
            colors=self.theme["stacktrail"],  # type: ignore [arg-type]
            frames_per_state=3,
        )
        self.visual_effects["stacktrans"] = ve_stacktrans
        ve_backtrans = ve.ColorTransition(
            layer=1,
            category=ve.STYLE,
            cells=[],
            transitioning=dict(),
            colors=self.theme["backtracktrail"],  # type: ignore [arg-type]
            frames_per_state=3,
        )
        self.visual_effects["backtrans"] = ve_backtrans
        while stack:
            ve_workingcell.cell = cell
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
            unvisited_neighbors = [neighbor for neighbor in neighbors if not neighbor.links]
            ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if neighbor.links]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.status_text["State"] = "Walking"
                self.maze.link_cells(cell, next_cell)
                ve_stacktrans.cells.append(next_cell)
                ve_lastlinked.cell = next_cell
                stack.append(next_cell)
                cell = next_cell
                self.status_text["Pending Paths"] = len(unvisited_neighbors)
                self.status_text["Stack Length"] = len(stack)
                yield self.maze

            else:
                stack.pop()
                if stack:
                    self.status_text["State"] = "Backtracking"
                    cell = stack[-1]
                    ve_backtrans.cells.append(cell)
                    ve_workingcell.cell = cell
                    self.status_text["Stack Length"] = len(stack)
                    if self.frame_wanted():
                        yield self.maze
        self.status_text["Stack Length"] = 0
        self.status_text["Pending Paths"] = 0
        self.status_text["State"] = "Complete"
        self.visual_effects.clear()
        yield self.maze
