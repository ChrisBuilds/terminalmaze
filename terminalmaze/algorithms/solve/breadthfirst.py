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
            layer=self.theme["frontier"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGIC,
            color=self.theme["frontier"]["color"],  # type: ignore [arg-type]
            cells=frontier,
        )
        self.visual_effects["frontier"] = ve_frontier

        ve_visited = ve.ColorMultipleCells(
            layer=self.theme["visited"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGICSTYLE,
            color=self.theme["visited"]["color"],  # type: ignore [arg-type]
            cells=visited,
        )
        self.visual_effects["visited"] = ve_visited

        ve_visited_transition = ve.ValueTransition(
            layer=self.theme["visited_transition"]["layer"],  # type: ignore [arg-type]
            category=ve.STYLE,
            colors=self.theme["visited_transition"]["colors"],  # type: ignore [arg-type]
            characters=self.theme["visited_transition"]["characters"],  # type: ignore [arg-type]
            cells=[],
            frames_per_value=self.theme["visited_transition"]["frames_per_value"],  # type: ignore [arg-type]
            transitioning=dict(),
        )
        self.visual_effects["visited_transition"] = ve_visited_transition

        ve_target = ve.ColorSingleCell(
            layer=self.theme["target"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGIC,
            color=self.theme["target"]["color"],  # type: ignore [arg-type]
            cell=target,
        )
        self.visual_effects["target"] = ve_target

        ve_workingcell = ve.ColorSingleCell(
            layer=self.theme["workingcell"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGIC,
            color=self.theme["workingcell"]["color"],  # type: ignore [arg-type]
            cell=start,
        )
        self.visual_effects["position"] = ve_workingcell

        ve_solutionpath = ve.ColorMultipleCells(
            layer=self.theme["solutionpath"]["layer"],  # type: ignore [arg-type]
            category=ve.LOGICSTYLE,
            color=self.theme["solutionpath"]["color"],  # type: ignore [arg-type]
            cells=[],
        )
        self.visual_effects["path"] = ve_solutionpath

        ve_solutiontransition = ve.ValueTransition(
            layer=self.theme["solution_transition"]["layer"],  # type: ignore [arg-type]
            category=ve.STYLE,
            colors=self.theme["solution_transition"]["colors"],  # type: ignore [arg-type]
            characters=self.theme["solution_transition"]["characters"],  # type: ignore [arg-type]
            cells=[],
            transitioning=dict(),
            frames_per_value=self.theme["solution_transition"]["frames_per_value"],  # type: ignore [arg-type]
        )
        self.visual_effects["solutiontransition"] = ve_solutiontransition

        while frontier:
            self.status_text["State"] = "Exploring"
            self.status_text["Frontier"] = len(frontier)
            self.status_text["Visited"] = len(visited)
            position = frontier.pop(0)
            visited.append(position)
            if position not in transitions:
                ve_visited_transition.cells.append(position)
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
