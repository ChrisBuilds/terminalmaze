from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.solve.solvealgorithm import SolveAlgorithm
import terminalmaze.tools.visualeffects as ve
from collections.abc import Generator


class BreadthFirst(SolveAlgorithm):
    def __init__(self, maze: Grid) -> None:
        super().__init__(maze)
        self.status_text["Algorithm"] = "Breadth First"

    def solve(self) -> Generator[Grid, None, None]:
        target = list(self.maze.each_cell())[-1]
        start = list(self.maze.each_cell())[0]
        frontier = [start]
        explored: dict[Cell, Cell] = {start: start}
        visited: list[Cell] = []
        ve_frontier = ve.ColorMultipleCells(layer=0, category=ve.LOGIC, color=231, cells=frontier)
        self.visual_effects["frontier"] = ve_frontier
        ve_visited = ve.ColorMultipleCells(layer=0, category=ve.STYLE, color=218, cells=visited)
        self.visual_effects["visited"] = ve_visited
        ve_target = ve.ColorSingleCell(layer=0, category=ve.LOGIC, color=202, cell=target)
        self.visual_effects["target"] = ve_target
        ve_position = ve.ColorSingleCell(layer=0, category=ve.LOGIC, color=218, cell=start)
        self.visual_effects["position"] = ve_position
        ve_path = ve.ColorMultipleCells(layer=1, category=ve.LOGIC, color=159, cells=[])
        self.visual_effects["path"] = ve_path
        ve_path_trail = ve.TrailingColor(
            layer=2,
            category=ve.STYLE,
            colors=[155, 156, 156, 156, 156, 156, 156, 156, 157, 157, 157, 157, 157, 157, 158, 158, 158, 158, 159],
            cells=[],
        )
        self.visual_effects["path_trail"] = ve_path_trail
        frame_gap = 1
        while frontier:
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(visited)
            position = frontier.pop(0)
            visited.append(position)
            ve_position.cell = position
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
                self.status_text["Time Elapsed"] = self.time_elapsed()
                yield self.maze
        self.status_text["Frontier"] = 0

        del self.visual_effects["frontier"]
        del self.visual_effects["position"]
        position = target
        route: list[Cell] = [target]
        if target not in explored:
            return
        while position != start:
            route.append(explored[position])
            position = explored[position]
        route.reverse()
        path: list[Cell] = list()
        ve_path.cells = path
        for step in route:
            path.append(step)
            ve_path_trail.cells = path[-len(ve_path_trail.colors) :][::-1]
            self.status_text["Solution Length"] = len(route)
            self.status_text["Time Elapsed"] = self.time_elapsed()
            yield self.maze
        while ve_path_trail.cells:
            ve_path_trail.cells.pop()
            self.status_text["Time Elapsed"] = self.time_elapsed()
            yield self.maze
        self.status_text["Time Elapsed"] = self.time_elapsed()
        yield self.maze
