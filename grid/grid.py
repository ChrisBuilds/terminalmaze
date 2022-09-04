from grid.cell import Cell
import random
import colored
from collections.abc import Generator


class Grid:
    def __init__(self, width: int, height: int, mask=None) -> None:
        """
        Create a new grid with the given width and height.

        :param width: the number of columns in the grid
        :param height: the number of rows in the grid
        """
        self.width: int = width
        self.height: int = height
        self.mask: list[str] = mask
        self.cells: dict[tuple[int, int], Cell] = {}
        self.masked_cells = {}
        self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self) -> None:
        """
        Create a dictionary of Cell objects, where the dictionary key is a tuple of the row and column, and
        the value is the Cell object.
        """
        for row in range(self.height):
            for col in range(self.width):
                cell = Cell(row, col)
                self.cells[(row, col)] = cell

        if self.mask:
            self.mask_cells()

    def mask_cells(self) -> None:
        """Translate mask string to cell coordinates centered in the grid. Track masked cells in self.masked_cells."""
        mask_midpoint_x = -(-len(max(self.mask)) // 2)
        mask_midpoint_y = -(-len(self.mask) // 2)
        grid_midpoint_x = -(-self.width // 2)
        grid_midpoint_y = -(-self.height // 2)
        x_delta = grid_midpoint_x - mask_midpoint_x
        y_delta = grid_midpoint_y - mask_midpoint_y
        for y, line in enumerate(self.mask):
            for x, symbol in enumerate(line):
                if symbol == "#":
                    cell_coordinates = (y + y_delta, x + x_delta)
                    self.masked_cells[cell_coordinates] = self.get_cell(cell_coordinates)

    def configure_cells(self) -> None:
        """
        For each cell in the grid, set the neighbors of that cell to the cells that are adjacent to it.
        """
        for cell in self.cells.values():
            row = cell.row
            col = cell.column
            adjacent_cell_coordinates = {
                "north": (row - 1, col),
                "south": (row + 1, col),
                "west": (row, col - 1),
                "east": (row, col + 1),
            }
            for direction, coordinates in adjacent_cell_coordinates.items():
                neighbor = self.get_cell(coordinates)
                if neighbor:
                    cell.neighbors[direction] = neighbor

    def get_cell(self, cell: tuple[int, int]) -> Cell:
        """
        Given cell coordinates, return the cell object if valid coordinates, else None.

        :param cell: a tuple of the form (row, column)
        :return: The cell object
        """
        row = cell[0]
        column = cell[1]
        if cell in self.cells:
            return self.cells[cell]
        else:
            return None

    def get_neighbors(self, cell: Cell, adjacent: bool = True) -> dict[str, Cell]:
        """
        Given a cell, return a list of its neighboring cells

        :param cell: the cell to get the neighbors of
        :param adjacent: ignore diagonal neighbors
        :return: A dict of {str,Cell} neighbors.
        """
        neighbors = {}
        for direction, neighbor in cell.neighbors.items():
            if neighbor not in self.masked_cells.values():
                neighbors[direction] = neighbor
        return neighbors

    def random_cell(self) -> Cell:
        """
        Return a random cell from the grid.
        :return: A random cell from the list of cells.
        """
        cell = random.choice(list(self.cells.values()))
        return cell

    def size(self) -> int:
        """
        Return the number of cells in the grid.
        :return: Number of cells in the grid
        """
        return self.height * self.width

    def each_row(self, bottom_up: bool = False) -> Generator[list[Cell], None, None]:
        """
        Yield one row of the grid at a time as a list.

        :param bottom_up: If True, the cells are traversed in bottom-up order, defaults to False (optional)
        """
        if not bottom_up:
            for row in range(self.height):
                yield [self.cells[(row, col)] for col in range(self.width)]
        else:
            for row in range(self.height - 1, -1, -1):
                yield [self.cells[(row, col)] for col in range(self.width)]

    def each_cell(self) -> Generator[Cell, None, None]:
        """
        Return a generator that yields a cell at a time.
        """
        for row in range(self.height):
            for col in range(self.width):
                yield self.cells[(row, col)]

    def get_visual_grid(self) -> list[list[str]]:
        """
        Create a grid of the maze, with a wall character between each cell.
        :return: A list of lists of strings.
        """
        cell: Cell

        self.visual_grid = []
        wall = f"{colored.fg(102)}{chr(9608)}"
        path = f"{colored.fg(106)}{chr(9608)}"
        for row in self.each_row():
            term_row = []
            lower_row = []
            for i, cell in enumerate(row):
                if cell.get_links():
                    term_row.append(path)
                else:
                    term_row.append(wall)
                cell_east = cell.neighbors.get("east")
                cell_south = cell.neighbors.get("south")
                if cell_east:
                    if cell.is_linked(cell_east):
                        term_row.append(path)
                    else:
                        term_row.append(wall)
                if cell_south:
                    if cell.is_linked(cell_south):
                        lower_row.append(path)
                    else:
                        lower_row.append(wall)
                    if i != len(row) - 1:
                        lower_row.append(wall)
            self.visual_grid.append(term_row)
            self.visual_grid.append(lower_row)
        self.visual_grid.pop(-1)  # remove extra lower row
        for row in self.visual_grid:
            row.insert(0, wall)
            row.append(wall)
        self.visual_grid.insert(0, [wall for _ in range(len(self.visual_grid[0]))])
        self.visual_grid.append([wall for _ in range(len(self.visual_grid[0]))])
        return self.visual_grid

    def __str__(self) -> str:
        """
        Prints a text representation of the maze.
        :return: A string representation of the grid.
        """
        output = "+" + "---+" * self.width + "\n"

        for row in self.each_row():
            top = "|"
            bottom = "+"
            for cell in row:
                body = "   "
                if cell.is_linked(self.get_cell(cell.neighbors["east"])):
                    eCelluth_boundary = "   "
                else:
                    south_boundary = "---"
                corner = "+"
                bottom += south_boundary + corner

            output += top + "\n"
            output += bottom + "\n"

        return output
