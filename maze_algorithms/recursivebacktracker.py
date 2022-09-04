from grid.grid import Grid, Cell
import random


class RecursiveBacktracker:
    def __init__(self, mazegrid: Grid, showlogic: bool = False) -> None:
        self.grid: Grid = mazegrid
        self.showlogic: bool = showlogic
        self.logic_data: dict[str, Cell] = {}

    def generate_maze(self) -> Grid:
        cell = self.grid.random_cell()
        stack = [cell]
        self.logic_data["logic0"] = stack
        while stack:
            self.logic_data["working_cell"] = cell
            unvisited_neighbors = [
                neighbor for neighbor in self.grid.get_neighbors(cell).values() if not neighbor.links
            ]
            self.logic_data["invalid_neighbors"] = [
                neighbor for neighbor in self.grid.get_neighbors(cell).values() if neighbor.links
            ]
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
