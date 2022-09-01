from grid import Grid
import random, time
from terminal_grid import TermGrid


class HuntandKill:
    def __init__(self, grid: Grid, screen):
        self.screen = screen
        self.grid = grid
        unvisited = [cell for cell in grid.cells.values()]
        cell = random.choice(unvisited)
        unvisited.remove(cell)
        while unvisited:
            unvisited_neighbors = [c for c in self.grid.get_neighbors(cell) if c in unvisited]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                cell.link(neighbor)
                unvisited.remove(neighbor)
                self.show_grid()
                time.sleep(0.05)
                cell = neighbor

            else:
                for cell in unvisited:
                    visited_neighbors = [c for c in self.grid.get_neighbors(cell) if c not in unvisited]
                    if visited_neighbors:
                        cell.link(random.choice(visited_neighbors))
                        unvisited.remove(cell)
                        self.show_grid()
                        break

    def show_grid(self):
        visual_grid = self.grid.get_visual_grid()
        termgrid = TermGrid(self.screen, len(visual_grid) + 2, len(visual_grid[0]) + 2)
        for row in range(len(visual_grid)):
            for col in range(len(visual_grid[0])):
                termgrid.cells[(row, col)] = visual_grid[row][col]
        termgrid.show()
