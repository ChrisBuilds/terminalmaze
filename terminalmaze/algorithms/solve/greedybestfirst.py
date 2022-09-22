from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from collections.abc import Generator
from terminalmaze.config import BreadthFirstTheme
from queue import PriorityQueue


class GreedyBestFirst(Algorithm):
    def __init__(self, maze: Grid, theme: BreadthFirstTheme, *conditions) -> None:
        super().__init__(maze)
        self.theme = theme
        self.conditions = conditions
        self.status_text["Algorithm"] = "Greedy Best First"
        self.status_text["Frontier"] = 0
        self.status_text["Visited"] = 0
        self.status_text["Position"] = ""
        self.status_text["Target"] = ""
        self.status_text["State"] = ""
        self.skipped_frames = 0

    def solve(self) -> Generator[Grid, None, None]:
        target = list(self.maze.each_cell())[-1]
        start = list(self.maze.each_cell())[0]
        frontier: PriorityQueue = PriorityQueue()
        frontier.put((0, start))
        explored: dict[Cell, Cell] = {start: start}
        transitions: set[Cell] = set()
        self.status_text["Target"] = f"({target.column}, {target.row})"

        ve_frontier = ve.ColorMultipleCells(self.theme.frontier)
        ve_frontier.cells.append(start)
        self.visual_effects["frontier"] = ve_frontier

        ve_visited = ve.ColorMultipleCells(self.theme.visited)
        self.visual_effects["visited"] = ve_visited

        ve_visited_transition = ve.ValueTransition(self.theme.visited_transition)
        self.visual_effects["visited_transition"] = ve_visited_transition

        ve_target = ve.ColorSingleCell(self.theme.target)
        self.visual_effects["target"] = ve_target

        ve_workingcell = ve.ColorSingleCell(self.theme.working_cell)
        self.visual_effects["position"] = ve_workingcell

        ve_solutionpath = ve.ColorMultipleCells(self.theme.solution_path)
        self.visual_effects["path"] = ve_solutionpath

        ve_solutiontransition = ve.ValueTransition(self.theme.solution_transition)
        self.visual_effects["solutiontransition"] = ve_solutiontransition

        while not frontier.empty():
            self.status_text["State"] = "Exploring"
            distance, position = frontier.get()
            self.status_text["Position"] = f"({position.column}, {position.row})"
            ve_frontier.cells.remove(position)
            ve_visited.cells.append(position)
            if position not in transitions:
                ve_visited_transition.cells.append(position)
            ve_workingcell.cell = position
            edges = [neighbor for neighbor in position.links if neighbor not in explored]
            for cell in edges:
                explored[cell] = position
                if cell == target:
                    frontier = PriorityQueue()
                    self.status_text["Position"] = f"({cell.column}, {cell.row})"
                    yield self.maze
                    break
                frontier.put((GreedyBestFirst.distance(cell, target), cell))
                ve_frontier.cells.append(cell)

            self.status_text["Frontier"] = frontier.qsize()
            self.status_text["Visited"] = len(ve_visited.cells)
            yield self.maze

        self.status_text["Frontier"] = 0
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
