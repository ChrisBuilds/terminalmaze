from terminalmaze.resources.grid import Grid
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from terminalmaze.config import RecursiveBacktrackerTheme
import random
from typing import Generator


class RecursiveBacktracker(Algorithm):
    def __init__(self, maze: Grid, theme: RecursiveBacktrackerTheme) -> None:
        super().__init__(maze)
        self.status_text["Algorithm"] = "Recursive Backtracker"
        self.status_text.update({"Pending Paths": "", "Stack Length": "", "State": ""})
        self.skip_frames = 1
        self.theme = theme

    def generate_maze(self) -> Generator[Grid, None, None]:
        cell = self.maze.random_cell()
        stack = [cell]

        ve_stack = ve.ColorMultipleCells(self.theme.stack)
        ve_stack.cells = stack
        self.visual_effects["stack"] = ve_stack

        ve_workingcell = ve.ColorSingleCell(self.theme.working_cell)
        ve_workingcell.cell = cell
        self.visual_effects["working_cell"] = ve_workingcell

        ve_invalidneighbors = ve.ColorMultipleCells(self.theme.invalid_neighbors)
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors

        ve_lastlinked = ve.ColorSingleCell(self.theme.last_linked)
        ve_lastlinked.cell = cell
        self.visual_effects["last_linked"] = ve_lastlinked

        ve_stack_transition = ve.ValueTransition(self.theme.stack_transition)
        self.visual_effects["stacktrans"] = ve_stack_transition

        ve_backtrack_transition = ve.ValueTransition(self.theme.backtrack_transition)
        self.visual_effects["backtrans"] = ve_backtrack_transition

        while stack:
            ve_workingcell.cell = cell
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
            unvisited_neighbors = [neighbor for neighbor in neighbors if not neighbor.links]
            ve_invalidneighbors.cells = [neighbor for neighbor in neighbors if neighbor.links]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.status_text["State"] = "Walking"
                self.maze.link_cells(cell, next_cell)
                ve_stack_transition.cells.append(next_cell)
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
                    ve_backtrack_transition.cells.append(cell)
                    ve_workingcell.cell = cell
                    self.status_text["Stack Length"] = len(stack)
                    if self.frame_wanted():
                        yield self.maze
        while ve_backtrack_transition.transitioning or ve_stack_transition.transitioning:
            yield self.maze
        self.status_text["Stack Length"] = 0
        self.status_text["Pending Paths"] = 0
        self.status_text["State"] = "Complete"
        self.visual_effects.clear()
        yield self.maze
