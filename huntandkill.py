from grid import Grid
import random, time
from os import system


class HuntandKill:
    def __init__(self, grid: Grid):
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
        lines = ["".join(line) for line in visual_grid]
        system("clear")
        print("\n".join(lines))
