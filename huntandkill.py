from grid import Grid
import random, time
from os import system


class HuntandKill:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.logic_data = {}

    def generate_maze(self):
        unvisited = [cell for cell in self.grid.cells.values()]
        cell = random.choice(unvisited)
        unvisited.remove(cell)
        while unvisited:
            unvisited_neighbors = [c for c in self.grid.get_neighbors(cell) if c in unvisited]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                cell.link(neighbor)
                unvisited.remove(neighbor)
                yield self.grid
                cell = neighbor

            else:
                for cell in unvisited:
                    visited_neighbors = [c for c in self.grid.get_neighbors(cell) if c not in unvisited]
                    if visited_neighbors:
                        cell.link(random.choice(visited_neighbors))
                        unvisited.remove(cell)
                        yield self.grid
                        break
