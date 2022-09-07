from grid.grid import Grid
from collections.abc import Generator


class BreadthFirst:
    def __init__(self, maze: Grid, showlogic: bool = False) -> None:
        self.maze = maze
        self.showlogic = showlogic
        self.logic_data = {}
        self.status_text = {"Algorithm": "Breadth First", "Seed": self.maze.seed}

    def solve(self) -> Generator[Grid, None, None]:
        target = list(self.maze.each_cell())[-1]
        self.logic_data["target"] = target
        start = list(self.maze.each_cell())[0]
        frontier = [start]
        explored = {start: None}
        visited = []
        self.logic_data["explored"] = visited
        self.logic_data["frontier"] = frontier
        frame_gap = 1
        while frontier:
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(visited)
            position = frontier.pop(0)
            visited.append(position)
            self.logic_data["position"] = position
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

        self.logic_data.pop("explored", None)
        self.logic_data.pop("frontier", None)
        self.logic_data.pop("position", None)
        position = target
        route = [target]
        if target not in explored:
            return
        while position != start:
            route.append(explored[position])
            position = explored[position]
        route.reverse()
        path = []
        self.logic_data["path"] = path
        for step in route:
            path.append(step)
            self.status_text["Solution Length"] = len(route)
            yield self.maze
