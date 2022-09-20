from terminalmaze.resources.grid import Grid, Cell
from terminalmaze.algorithms.algorithm import Algorithm
import terminalmaze.tools.visualeffects as ve
from collections.abc import Generator


class BreadthFirst(Algorithm):
    def __init__(self, maze: Grid, theme: ve.Theme) -> None:
        super().__init__(maze)
        self.theme = theme["breadthfirst"]
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
        visited: list[Cell] = []
        transitions: set[Cell] = set()
        ve_frontier = ve.ColorMultipleCells(
            layer=0, category=ve.LOGIC, color=self.theme["frontier"], cells=frontier  # type: ignore [arg-type]
        )
        self.visual_effects["frontier"] = ve_frontier
        ve_visited = ve.ColorMultipleCells(
            layer=0, category=ve.LOGICSTYLE, color=self.theme["visited"], cells=visited  # type: ignore [arg-type]
        )
        self.visual_effects["visited"] = ve_visited
        ve_visited_color_transition = ve.ColorTransition(
            layer=1,
            category=ve.STYLE,
            colors=self.theme["visited_color_transition"],  # type: ignore [arg-type]
            cells=[],
            frames_per_state=10,
            transitioning=dict(),
        )
        self.visual_effects["visited_transition"] = ve_visited_color_transition
        ve_visited_character_transition = ve.CharacterTransition(
            layer=1,
            category=ve.STYLE,
            characters=self.theme["visited_character_transition"],  # type: ignore [arg-type]
            cells=[],
            frames_per_state=10,
            transitioning=dict(),
        )
        self.visual_effects["visited_character_transition"] = ve_visited_character_transition
        ve_target = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, color=self.theme["target"], cell=target  # type: ignore [arg-type]
        )
        self.visual_effects["target"] = ve_target
        ve_workingcell = ve.ColorSingleCell(
            layer=0, category=ve.LOGIC, color=self.theme["workingcell"], cell=start  # type: ignore [arg-type]
        )
        self.visual_effects["position"] = ve_workingcell
        ve_solutionpath = ve.ColorMultipleCells(
            layer=1, category=ve.LOGICSTYLE, color=self.theme["solutionpath"], cells=[]  # type: ignore [arg-type]
        )
        self.visual_effects["path"] = ve_solutionpath
        ve_pathtransition = ve.ColorTransition(
            layer=2,
            category=ve.STYLE,
            colors=self.theme["visited_color_transition"],  # type: ignore [arg-type]
            cells=[],
            transitioning=dict(),
            frames_per_state=1,
        )
        self.visual_effects["pathtransition"] = ve_pathtransition
        ve_solutiontransition = ve.ColorTransition(
            layer=2,
            category=ve.STYLE,
            colors=self.theme["solutiontransition"],  # type: ignore [arg-type]
            cells=[],
            transitioning=dict(),
            frames_per_state=1,
        )
        self.visual_effects["solutiontransition"] = ve_solutiontransition
        while frontier:
            self.status_text["State"] = "Exploring"
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(visited)
            position = frontier.pop(0)
            visited.append(position)
            if position not in transitions:
                ve_visited_color_transition.cells.append(position)
                ve_visited_character_transition.cells.append(position)
            ve_workingcell.cell = position
            edges = [neighbor for neighbor in position.links if neighbor not in explored and neighbor not in frontier]
            for cell in edges:
                explored[cell] = position
            frontier.extend(edges)
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(visited)
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
