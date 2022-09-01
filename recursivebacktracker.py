from grid import Grid
import random


class RecursiveBacktracker:
    def __init__(self, grid: Grid):
        self.grid = grid

    def generate_maze(self):
        cell = self.grid.random_cell()
        stack = []
        stack.append(cell)
        while stack:
            unvisited_neighbors = [c for c in self.grid.get_neighbors(cell) if not c.links]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                cell.link(next_cell)
                stack.append(next_cell)
                cell = next_cell
                yield self.grid

            else:
                stack.pop()
                if stack:
                    cell = stack[-1]
