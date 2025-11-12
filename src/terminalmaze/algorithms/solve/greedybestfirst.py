from collections.abc import Generator
from queue import PriorityQueue

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import BreadthFirstTheme
from terminalmaze.resources.grid import Cell, Grid


class GreedyBestFirst(Algorithm):
    def __init__(self, maze: Grid, theme: BreadthFirstTheme, *conditions) -> None:
        super().__init__(maze, theme)
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

        ve_frontier = ve.ModifyMultipleCells(self.theme.frontier)
        ve_frontier.cells.append(start)
        self.visual_effects["frontier"] = ve_frontier

        ve_visited = ve.ModifyMultipleCells(self.theme.visited)
        self.visual_effects["visited"] = ve_visited

        ve_visited_animation = ve.Animation(self.theme.visited_animation)
        self.visual_effects["visited_transition"] = ve_visited_animation

        ve_target = ve.ModifySingleCell(self.theme.target)
        self.visual_effects["target"] = ve_target

        ve_working_cell = ve.ModifySingleCell(self.theme.working_cell)
        self.visual_effects["position"] = ve_working_cell

        ve_solution_path = ve.ModifyMultipleCells(self.theme.solution_path)
        self.visual_effects["path"] = ve_solution_path

        ve_solution_animation = ve.Animation(self.theme.solution_animation)
        self.visual_effects["solutiontransition"] = ve_solution_animation

        while not frontier.empty():
            self.status_text["State"] = "Exploring"
            distance, position = frontier.get()
            self.status_text["Position"] = f"({position.column}, {position.row})"
            ve_frontier.cells.remove(position)
            ve_visited.cells.append(position)
            if position not in transitions:
                ve_visited_animation.cells.append(position)
            ve_working_cell.cell = position
            edges = [neighbor for neighbor in position.links if neighbor not in explored]
            for cell in edges:
                explored[cell] = position
                if cell == target:
                    frontier = PriorityQueue()
                    self.status_text["Position"] = f"({cell.column}, {cell.row})"
                    ve_visited.cells.append(cell)
                    ve_visited_animation.cells.append(cell)
                    yield self.maze
                    break
                frontier.put((GreedyBestFirst.distance(cell, target), cell))
                ve_frontier.cells.append(cell)

            self.status_text["Frontier"] = frontier.qsize()
            self.status_text["Visited"] = len(ve_visited.cells)
            yield self.maze

        while ve_visited_animation.animating:
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
        ve_solution_path.cells = path
        for step in route:
            self.status_text["State"] = "Solved"
            path.append(step)
            ve_solution_animation.cells.append(step)
            self.status_text["Solution Length"] = len(route)
            yield self.maze
        while ve_solution_animation.animating:
            yield self.maze
        yield self.maze
