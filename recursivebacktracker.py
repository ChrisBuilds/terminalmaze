from grid import Grid
import random, time
from os import system


class RecursiveBacktracker:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.visual_algo = True
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
                self.show_grid()
                time.sleep(0.05)
            else:
                stack.pop()
                if stack:
                    cell = stack[-1]

    def show_grid(self):
        visual_grid = self.grid.get_visual_grid()
        lines = ["".join(line) for line in visual_grid]
        system("clear")
        print("\n".join(lines))
