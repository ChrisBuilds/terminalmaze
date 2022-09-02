from grid import Grid
import random, time
from os import system


class HuntandKill:
    def __init__(self, grid: Grid, showlogic=False):
        self.grid = grid
        self.logic_data = {}

    def generate_maze(self):
        unvisited = [cell for cell in self.grid.cells.values()]
        cell = random.choice(unvisited)
        unvisited.remove(cell)
        while unvisited:
            self.logic_data["working_cell"] = cell
            unvisited_neighbors = [c for c in self.grid.get_neighbors(cell) if c in unvisited]
            if unvisited_neighbors:
                neighbor = random.choice(unvisited_neighbors)
                cell.link(neighbor)
                self.logic_data["last_linked"] = neighbor
                unvisited.remove(neighbor)
                cell = neighbor
                yield self.grid

            else:
                for cell in unvisited:
                    self.logic_data["working_cell"] = cell
                    visited_neighbors = [c for c in self.grid.get_neighbors(cell) if c not in unvisited]
                    yield self.grid
                    if visited_neighbors:
                        neighbor = random.choice(visited_neighbors)
                        cell.link(neighbor)
                        self.logic_data["last_linked"] = neighbor
                        unvisited.remove(cell)
                        break
                yield self.grid
