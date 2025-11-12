import random
from typing import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import RecursiveBacktrackerTheme
from terminalmaze.resources.grid import Grid


class RecursiveBacktracker(Algorithm):
    def __init__(self, maze: Grid, theme: RecursiveBacktrackerTheme) -> None:
        super().__init__(maze, theme)
        self.status_text["Algorithm"] = "Recursive Backtracker"
        self.status_text.update({"Pending Paths": "", "Stack Length": "", "State": ""})
        self.skip_frames = theme.backtrack_skip_frames
        self.theme = theme

    def generate_maze(self) -> Generator[Grid, None, None]:
        cell = self.maze.random_cell()
        stack = [cell]

        ve_working_cell = ve.Animation(self.theme.working_cell)
        ve_working_cell.cells.append(cell)
        self.visual_effects["working_cell"] = ve_working_cell

        ve_stack = ve.ModifyMultipleCells(self.theme.stack)
        ve_stack.cells = stack
        self.visual_effects["stack"] = ve_stack

        ve_invalid_neighbors = ve.Animation(self.theme.invalid_neighbors)
        self.visual_effects["invalid_neighbors"] = ve_invalid_neighbors

        ve_last_linked = ve.Animation(self.theme.last_linked)
        ve_last_linked.cells.append(cell)
        self.visual_effects["last_linked"] = ve_last_linked

        ve_stack_added_cells = ve.Animation(self.theme.stack_added_cells)
        self.visual_effects["stacktrans"] = ve_stack_added_cells

        ve_stack_removed_cells = ve.Animation(self.theme.stack_removed_cells)
        self.visual_effects["backtrans"] = ve_stack_removed_cells

        while stack:
            ve_working_cell.cells.append(cell)
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(cell).values() if neighbor]
            unvisited_neighbors = [neighbor for neighbor in neighbors if not neighbor.links]
            ve_invalid_neighbors.cells.extend([neighbor for neighbor in neighbors if neighbor.links])
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.status_text["State"] = "Walking"
                self.maze.link_cells(cell, next_cell)
                ve_stack_added_cells.cells.append(next_cell)
                ve_last_linked.cells.append(next_cell)
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
                    ve_stack_removed_cells.cells.append(cell)
                    ve_working_cell.cells.append(cell)
                    self.status_text["Stack Length"] = len(stack)
                    if self.frame_wanted():
                        yield self.maze
        while ve_stack_removed_cells.animating or ve_stack_added_cells.animating:
            yield self.maze
        self.status_text["Stack Length"] = 0
        self.status_text["Pending Paths"] = 0
        self.status_text["State"] = "Complete"
        self.visual_effects.clear()
        yield self.maze
