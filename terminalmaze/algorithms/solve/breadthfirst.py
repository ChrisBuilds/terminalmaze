from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.solve.solvealgorithm import SolveAlgorithm
from collections.abc import Generator


class BreadthFirst(SolveAlgorithm):
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        super().__init__(maze, showlogic)
        self.status_text["Algorithm"] = "Breadth First"

    def solve(self) -> Generator[Grid, None, None]:
        target = list(self.maze.each_cell())[-1]
        self.visual_effects["target"] = target
        start = list(self.maze.each_cell())[0]
        frontier = [start]
        explored: dict[Cell, Cell] = {start: start}
        visited: list[Cell] = []
        self.visual_effects["explored"] = visited
        self.visual_effects["frontier"] = frontier
        frame_gap = 1
        while frontier:
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(visited)
            position = frontier.pop(0)
            visited.append(position)
            self.visual_effects["position"] = position
            edges = [neighbor for neighbor in position.links if neighbor not in explored and neighbor not in frontier]
            for cell in edges:
                explored[cell] = position
            frontier.extend(edges)
            frame_gap -= 1
            if frame_gap == 0:
                frame_gap = len(frontier)
                frame_gap = 5
                self.status_text["Frontier"] = len(frontier)
                self.status_text["Visited"] = len(visited)
                yield self.maze

        self.visual_effects.pop("explored", None)
        self.visual_effects.pop("frontier", None)
        self.visual_effects.pop("position", None)
        position = target
        route: list[Cell] = [target]
        if target not in explored:
            return
        while position != start:
            route.append(explored[position])
            position = explored[position]
        route.reverse()
        path: list[Cell] = list()
        self.visual_effects["path"] = path
        for step in route:
            path.append(step)
            self.status_text["Solution Length"] = len(route)
            yield self.maze
