import random
import time
from os import system

from grid.grid import Grid


class AldousBroder:
    def __init__(self, mazegrid: Grid):
        self.grid = mazegrid
        unvisited = [cell for cell in mazegrid.cells]
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
        lines = ["".join(line) for line in visual_grid]
        system("clear")
        print("\n".join(lines))
