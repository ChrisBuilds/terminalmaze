from terminalmaze.resources.grid import Grid
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
            layer=self.theme["stack"]["layer"],  # type: ignore [arg-type]
            category=ve.STYLE,
            color=self.theme["stack"]["color"],  # type: ignore [arg-type]
            cells=stack,
        )
        self.visual_effects["stack"] = ve_stack

        ve_workingcell = ve.ColorSingleCell(
            layer=self.theme["workingcell"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGIC,
            color=self.theme["workingcell"]["color"],  # type: ignore [arg-type]
            cell=cell,
        )
        self.visual_effects["working_cell"] = ve_workingcell

        ve_invalidneighbors = ve.ColorMultipleCells(
            layer=self.theme["invalid_neighbors"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGIC,
            color=self.theme["invalid_neighbors"]["color"],  # type: ignore [arg-type]
            cells=[],
        )
        self.visual_effects["invalid_neighbors"] = ve_invalidneighbors

        ve_lastlinked = ve.ColorSingleCell(
            layer=self.theme["last_linked"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGIC,
            color=self.theme["last_linked"]["color"],  # type: ignore [arg-type]
            cell=cell,
        )
        self.visual_effects["last_linked"] = ve_lastlinked

        ve_stack_transition = ve.ValueTransition(
            layer=self.theme["stack_transition"]["layer"],  # type: ignore [arg-type]
            category=ve.STYLE,
            cells=[],
            transitioning=dict(),
            colors=self.theme["stack_transition"]["colors"],  # type: ignore [arg-type]
            characters=self.theme["stack_transition"]["characters"],  # type: ignore [arg-type]
            frames_per_value=self.theme["stack_transition"]["frames_per_value"],  # type: ignore [arg-type]
        )
        self.visual_effects["stacktrans"] = ve_stack_transition

        ve_backtrack_transition = ve.ValueTransition(
            layer=self.theme["backtrack_transition"]["layer"],  # type: ignore [arg-type]
            category=ve.STYLE,
            cells=[],
            transitioning=dict(),
            colors=self.theme["backtrack_transition"]["colors"],  # type: ignore [arg-type]
            characters=self.theme["backtrack_transition"]["characters"],  # type: ignore [arg-type]
            frames_per_value=self.theme["backtrack_transition"]["frames_per_value"],  # type: ignore [arg-type]
        )
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
