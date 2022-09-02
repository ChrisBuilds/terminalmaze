import random
import time
from os import system

from grid.grid import Grid


class BinaryTree:
    def __init__(self, grid: Grid):
        """
        Create a maze by randomly connecting each cell to its neighbor to the north or east.

        :param grid: The grid to be used for the simulation
        :type grid: Grid
        """

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
        lines = ["".join(line) for line in visual_grid]
        system("clear")
        print("\n".join(lines))
