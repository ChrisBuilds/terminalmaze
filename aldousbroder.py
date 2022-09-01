from grid import Grid
import random, time
from terminal_grid import TermGrid


class AldousBroder:
    def __init__(self, grid: Grid, screen):
        self.screen = screen
        self.grid = grid
        unvisited = [cell for cell in grid.cells]
        starting_cell_coords = random.choice(unvisited)
        unvisited.remove(starting_cell_coords)
        cell = self.grid.get_cell(starting_cell_coords)
        while unvisited:
            neighbor_coords = list(cell.neighbors.values())
            verified_neighbors = []
            for n in neighbor_coords:
                if self.grid.get_cell(n):
                    verified_neighbors.append(n)
            neighbor = random.choice(verified_neighbors)
            if neighbor in unvisited:
                cell.link(self.grid.get_cell(neighbor))
                unvisited.remove(neighbor)
                self.show_grid()
                time.sleep(0.1)
            cell = self.grid.get_cell(neighbor)

    def show_grid(self):
        visual_grid = self.grid.get_visual_grid()
        termgrid = TermGrid(self.screen, len(visual_grid) + 2, len(visual_grid[0]) + 2)
        for row in range(len(visual_grid)):
            for col in range(len(visual_grid[0])):
                termgrid.cells[(row, col)] = visual_grid[row][col]
        termgrid.show()
