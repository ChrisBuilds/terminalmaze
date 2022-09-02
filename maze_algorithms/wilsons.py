import random
from collections.abc import Generator


from grid.grid import Grid


class Wilsons:
    def __init__(self, grid: Grid, showlogic: bool = False) -> None:
        self.grid = grid
        self.showlogic = showlogic
        self.logic_data = {"working_cell": None, "last_linked": None}

    def generate_maze(self) -> Generator[Grid, None, None]:
        walk = []
        starting_target = self.grid.get_cell(random.choice(list(self.grid.cells.keys())))
        unvisited = list(self.grid.cells.keys())
        unvisited.remove((starting_target.row, starting_target.column))
        while unvisited:
            walk = []
            walking = True
            origin = self.grid.get_cell(random.choice(unvisited))
            walk.append((origin.row, origin.column))
            while walking:
                neighbors = []
                for coord in list(origin.neighbors.values()):
                    if self.grid.get_cell(coord):
                        neighbors.append(coord)
                next_cell = random.choice(neighbors)
                if next_cell in walk:
                    walk = walk[: walk.index(next_cell) + 1]
                    origin = self.grid.get_cell(walk[-1])
                elif next_cell not in unvisited:
                    walking = False
                    for cell in walk:
                        unvisited.remove(cell)
                    for i, cell in enumerate(walk):
                        if i == len(walk) - 1:
                            self.grid.get_cell(cell).link(self.grid.get_cell(next_cell))
                        else:
                            self.grid.get_cell(cell).link(self.grid.get_cell(walk[i + 1]))
                        yield self.grid
                else:
                    walk.append(next_cell)
                    origin = self.grid.get_cell(next_cell)
