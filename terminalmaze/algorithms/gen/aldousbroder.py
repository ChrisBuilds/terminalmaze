import random
import time
from collections.abc import Generator


from terminalmaze.resources.grid import Grid


class AldousBroder:
    def __init__(self, maze: Grid, showlogic: bool = False) -> Generator[Grid, None, None]:
        self.maze = maze
        self.showlogic = showlogic
        self.logic_data = {}
        self.status_text = {"Algorithm": "Aldous Broder", "Seed": self.maze.seed}
        self.last_linked = list()
        self.logic_data["last_linked"] = self.last_linked
        self.frame_time = time.time()
        random.seed(self.maze.seed)

    def generate_maze(self):
        unvisited = set(self.maze.each_cell())
        working_cell = unvisited.pop()
        self.logic_data["working_cell"] = working_cell
        if self.showlogic:
            self.status_text["Unvisited"] = len(unvisited)
            self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
            yield self.maze
        while unvisited:
            invalid_neighbors = [
                neighbor for neighbor in self.maze.get_neighbors(working_cell).values() if neighbor not in unvisited
            ]
            self.logic_data["invalid_neighbors"] = invalid_neighbors
            neighbor = random.choice([neighbor for neighbor in self.maze.get_neighbors(working_cell).values()])
            if neighbor in unvisited:
                self.maze.link_cells(working_cell, neighbor)
                self.last_linked.append(neighbor)
                if len(self.last_linked) == 10:
                    self.last_linked.pop(0)
                unvisited.discard(neighbor)
                self.status_text["Unvisited"] = len(unvisited)
                self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                yield self.maze
            working_cell = neighbor
            self.logic_data["working_cell"] = working_cell
            if self.showlogic:
                time_since_last_frame = time.time() - self.frame_time
                if time_since_last_frame > 0.10:
                    self.frame_time = time.time()
                    self.status_text["Unvisited"] = len(unvisited)
                    self.status_text["Cell"] = f"({working_cell.row},{working_cell.column})"
                    yield self.maze
