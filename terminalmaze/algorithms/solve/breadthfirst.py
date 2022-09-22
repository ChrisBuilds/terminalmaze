from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from collections.abc import Generator
from terminalmaze.config import BreadthFirstTheme


class BreadthFirst(Algorithm):
    def __init__(self, maze: Grid, theme: BreadthFirstTheme) -> None:
        super().__init__(maze)
        self.theme = theme
        self.status_text["Algorithm"] = "Breadth First"
        self.status_text["Frontier"] = 0
        self.status_text["Visited"] = 0
        self.status_text["Position"] = ""
        self.status_text["State"] = ""
        self.skipped_frames = 0

    def solve(self) -> Generator[Grid, None, None]:
        target = list(self.maze.each_cell())[-1]
        start = list(self.maze.each_cell())[0]
        frontier = [start]
        explored: dict[Cell, Cell] = {start: start}
        transitions: set[Cell] = set()

        ve_frontier = ve.ColorMultipleCells(ve.LOGIC, self.theme.frontier)
        ve_frontier.cells = frontier
        self.visual_effects["frontier"] = ve_frontier

        ve_visited = ve.ColorMultipleCells(ve.LOGICSTYLE, self.theme.visited)
        self.visual_effects["visited"] = ve_visited

        ve_visited_transition = ve.ValueTransition(ve.STYLE, self.theme.visited_transition)
        self.visual_effects["visited_transition"] = ve_visited_transition

        ve_target = ve.ColorSingleCell(ve.LOGIC, self.theme.target)
        self.visual_effects["target"] = ve_target

        ve_workingcell = ve.ColorSingleCell(ve.LOGIC, self.theme.working_cell)
        self.visual_effects["position"] = ve_workingcell

        ve_solutionpath = ve.ColorMultipleCells(ve.LOGICSTYLE, self.theme.solution_path)
        self.visual_effects["path"] = ve_solutionpath

        ve_solutiontransition = ve.ValueTransition(ve.STYLE, self.theme.solution_transition)
        self.visual_effects["solutiontransition"] = ve_solutiontransition

        while frontier:
            self.status_text["State"] = "Exploring"
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(ve_visited.cells)
            position = frontier.pop(0)
            ve_visited.cells.append(position)
            if position not in transitions:
                ve_visited_transition.cells.append(position)
            ve_workingcell.cell = position
            edges = [neighbor for neighbor in position.links if neighbor not in explored and neighbor not in frontier]
            for cell in edges:
                explored[cell] = position
            frontier.extend(edges)
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(ve_visited.cells)
            if self.frame_wanted_relative(frontier, divisor=4):
                yield self.maze

        self.status_text["Frontier"] = 0
        # del self.visual_effects["frontier"]
        del self.visual_effects["position"]
        position = target
        route: list[Cell] = [target]
        if target not in explored:
            return
        while position != start:
            self.status_text["State"] = "Pathing"
            route.append(explored[position])
            position = explored[position]
        route.reverse()
        path: list[Cell] = list()
        ve_solutionpath.cells = path
        for step in route:
            self.status_text["State"] = "Solved"
            path.append(step)
            ve_solutiontransition.cells.append(step)
            self.status_text["Solution Length"] = len(route)
            yield self.maze
        while ve_solutiontransition.transitioning:
            yield self.maze
        yield self.maze
