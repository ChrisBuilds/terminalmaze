from grid import Grid
import random


class RecursiveBacktracker:
    def __init__(self, grid: Grid, showlogic=False):
        self.grid = grid
        self.showlogic = showlogic
        self.logic_data = {"working_cell": None, "last_linked": None}

    def generate_maze(self) -> Grid:
        cell = self.grid.random_cell()
        stack = []
        stack.append(cell)
        while stack:
            self.logic_data["working_cell"] = cell
            unvisited_neighbors = [c for c in self.grid.get_neighbors(cell) if not c.links]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                cell.link(next_cell)
                self.logic_data["last_linked"] = next_cell
                stack.append(next_cell)
                cell = next_cell
                yield self.grid

            else:
                stack.pop()
                if stack:
                    cell = stack[-1]
                    if self.showlogic:
                        self.logic_data["working_cell"] = cell
                        yield self.grid
