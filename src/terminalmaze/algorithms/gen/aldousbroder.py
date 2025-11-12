import random
import time
from collections.abc import Generator

import terminalmaze.visual.visualeffects as ve
from terminalmaze.algorithms.algorithm import Algorithm
from terminalmaze.config import AldousBroderTheme
from terminalmaze.resources.grid import Grid


class AldousBroder(Algorithm):
    def __init__(self, maze: Grid, theme: AldousBroderTheme) -> None:
        super().__init__(maze, theme)
        self.status_text["Algorithm"] = "Aldous Broder"
        self.status_text.update({"Unvisited": 0, "Revisited": 0, "Cell": "", "State": ""})
        self.frame_time = time.time()
        self.theme = theme

    def generate_maze(self) -> Generator[Grid, None, None]:
        unvisited = set(self.maze.each_cell())
        working_cell = unvisited.pop()
        ve_working_cell = ve.Animation(self.theme.working_cell)
        ve_working_cell.cells.append(working_cell)
        self.visual_effects["working_cell"] = ve_working_cell
        ve_last_linked = ve.Animation(self.theme.last_linked)
        self.visual_effects["last_linked"] = ve_last_linked
        ve_invalid_neighbors = ve.Animation(self.theme.invalid_neighbors)
        self.visual_effects["invalid_neighbors"] = ve_invalid_neighbors
        ve_invalid_visited = ve.Animation(self.theme.invalid_visited)
        self.visual_effects["invalid_visited"] = ve_invalid_visited
        revisited = 0
        while unvisited:
            neighbors = [neighbor for neighbor in self.maze.get_neighbors(working_cell).values() if neighbor]
            ve_invalid_neighbors.cells.extend([neighbor for neighbor in neighbors if neighbor not in unvisited])
            neighbor = random.choice(neighbors)
            if neighbor in unvisited:
                self.maze.link_cells(working_cell, neighbor)
                ve_last_linked.cells.append(neighbor)
                unvisited.discard(neighbor)
                self.status_text["Unvisited"] = len(unvisited)
                self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                self.status_text["State"] = "Linking"
                yield self.maze
            else:
                revisited += 1
                self.status_text["Revisited"] = revisited
                self.status_text["State"] = "Searching"
                if neighbor not in ve_invalid_visited.cells:
                    ve_invalid_visited.cells.append(neighbor)
                ve_invalid_visited.cells = ve_invalid_visited.cells[-50:]
                time_since_last_frame = time.time() - self.frame_time
                if time_since_last_frame > self.theme.maximum_searching_frame_delay:
                    self.frame_time = time.time()
                    self.status_text["Unvisited"] = len(unvisited)
                    self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"

                    yield self.maze

            working_cell = neighbor
            ve_working_cell.cells.append(working_cell)
        del self.visual_effects["working_cell"]
        del self.visual_effects["invalid_neighbors"]
        while ve_invalid_visited.animating or ve_last_linked.animating:
            yield self.maze
        self.status_text["State"] = "Complete"
        yield self.maze
