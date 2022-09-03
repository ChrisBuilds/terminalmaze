import random
from collections.abc import Generator


from grid.grid import Grid, Cell


class Wilsons:
    def __init__(self, grid: Grid, showlogic: bool = False) -> None:
        self.grid = grid
        self.showlogic = showlogic
        self.logic_data = {}

    def generate_maze(self) -> Generator[Grid, None, None]:
        walk: list[Cell] = []
        target = self.grid.random_cell()
        self.logic_data["logic1"] = target
        unvisited_cells = [cell for cell in self.grid.cells.values()]
        unvisited_cells.remove(target)
        while unvisited_cells:
            walk = []
            self.logic_data["logic0"] = walk
            walking = True
            working_cell = random.choice(unvisited_cells)
            self.logic_data["working_cell"] = working_cell
            walk.append(working_cell)
            while walking:
                next_cell = random.choice([neighbor for neighbor in working_cell.neighbors.values()])
                if next_cell in walk:
                    walk = walk[: walk.index(next_cell) + 1]
                    self.logic_data["logic0"] = walk
                    working_cell = walk[-1]
                    self.logic_data["working_cell"] = working_cell
                elif next_cell not in unvisited_cells:
                    walking = False
                    for i, cell in enumerate(walk):
                        if cell == walk[-1]:
                            cell.link(next_cell)
                        else:
                            cell.link(walk[i + 1])
                        unvisited_cells.remove(cell)
                        yield self.grid
                    self.logic_data.pop("logic1")
                else:
                    walk.append(next_cell)
                    working_cell = next_cell
                    self.logic_data["working_cell"] = working_cell
                    yield self.grid
