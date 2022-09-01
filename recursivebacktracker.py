from grid import Grid
import random, time
from terminal_grid import TermGrid


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
        # termgrid = TermGrid(self.screen, len(visual_grid) + 2, len(visual_grid[0]) + 2)
        # for row in range(len(visual_grid)):
        #    for col in range(len(visual_grid[0])):
        #        termgrid.cells[(row, col)] = visual_grid[row][col]
        # termgrid.show()
