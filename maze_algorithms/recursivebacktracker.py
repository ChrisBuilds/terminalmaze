from grid.grid import Grid, Cell
import random


class RecursiveBacktracker:
    def __init__(self, mazegrid: Grid, showlogic: bool = False) -> None:
        self.grid: Grid = mazegrid
        self.showlogic: bool = showlogic
        self.logic_data: dict[str, Cell] = {"working_cell": None, "last_linked": None}

    def generate_maze(self) -> Grid:
        cell = self.grid.random_cell()
        stack = [cell]
        while stack:
            self.logic_data["working_cell"] = cell
            unvisited_neighbors = [neighbor for neighbor in cell.neighbors.values() if not neighbor.links]
            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                cell.link(next_cell)
                self.logic_data["last_linked"] = next_cell
                stack.append(next_cell)
                cell = next_cell
                yield self.grid

            else:
                stack.pop()
                if stack:
                    cell = stack[-1]
                    if self.showlogic:
                        self.logic_data["working_cell"] = cell
                        yield self.grid
