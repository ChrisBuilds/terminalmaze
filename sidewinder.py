from grid import Grid
import random, time
from terminal_grid import TermGrid


class Sidewinder:
    def __init__(self, grid: Grid, screen):
        """
        For each row, randomly link cells in a run of cells to their north or east neighbor.

        :param grid: The grid to generate
        :type grid: Grid
        """
        self.grid = grid
        self.screen = screen
        for row in self.grid.each_row(bottom_up=True):
            run = []
            for cell in row:
                neighbors = {}
                directions = ("north", "east")
                for direction in directions:
                    neighbor_coord = cell.neighbors[direction]
                    if self.grid.get_cell(neighbor_coord):
                        neighbors[direction] = self.grid.get_cell(neighbor_coord)
                if neighbors:
                    link_direction = random.choice(list(neighbors.keys()))
                    run.append(cell)
                    if link_direction == "north":
                        cell = random.choice(run)
                        cell.link(grid.get_cell(cell.neighbors["north"]))
                        run = []
                    elif link_direction == "east":
                        cell.link(neighbors[link_direction])
                self.show_grid()
                time.sleep(0.05)

    def show_grid(self):
        visual_grid = self.grid.get_visual_grid()
        termgrid = TermGrid(self.screen, len(visual_grid) + 2, len(visual_grid[0]) + 2)
        for row in range(len(visual_grid)):
            for col in range(len(visual_grid[0])):
                termgrid.cells[(row, col)] = visual_grid[row][col]
        termgrid.show()
