from grid import Grid
import random, time
from terminal_grid import TermGrid


class BinaryTree:
    def __init__(self, grid: Grid, screen):
        """
        Create a maze by randomly connecting each cell to its neighbor to the north or east.

        :param grid: The grid to be used for the simulation
        :type grid: Grid
        """

        self.screen = screen
        self.grid = grid
        for cell in grid.each_cell():
            neighbors = []
            for direction in ("north", "east"):
                neighbor_coords = cell.neighbors[direction]
                if neighbor_coords in self.grid.cells:
                    neighbors.append(self.grid.get_cell(neighbor_coords))
            if neighbors:
                neighbor = random.choice(neighbors)
                cell.link(neighbor)
            self.show_grid()
            time.sleep(0.05)

    def show_grid(self):
        visual_grid = self.grid.get_visual_grid()
        termgrid = TermGrid(self.screen, len(visual_grid) + 2, len(visual_grid[0]) + 2)
        for row in range(len(visual_grid)):
            for col in range(len(visual_grid[0])):
                termgrid.cells[(row, col)] = visual_grid[row][col]
        termgrid.show()
