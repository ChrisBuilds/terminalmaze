import random
from collections.abc import Generator


from grid.grid import Grid


class AldousBroder:
    def __init__(self, mazegrid: Grid, showlogic: bool = False) -> Generator[Grid, None, None]:
        self.grid = mazegrid
        self.showlogic = showlogic
        self.logic_data = {}

    def generate_maze(self):
        unvisited = [cell for cell in self.grid.cells.values()]
        working_cell = random.choice(unvisited)
        self.logic_data["working_cell"] = working_cell
        if self.showlogic:
            yield self.grid
        unvisited.remove(working_cell)
        while unvisited:
            neighbor = random.choice([neighbor for neighbor in working_cell.neighbors.values()])
            if neighbor in unvisited:
                working_cell.link(neighbor)
                unvisited.remove(neighbor)
                yield self.grid
            working_cell = neighbor
            self.logic_data["working_cell"] = working_cell
            if self.showlogic:
                yield self.grid
