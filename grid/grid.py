from grid.cell import Cell
import random


class Grid:
    def __init__(self, width, height, mask=None):
        """
        Create a new grid with the given width and height.

        :param width: the number of columns in the grid
        :param height: the number of rows in the grid
        """
        self.width = width
        self.height = height
        self.cells = {}
        self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self):
        """
        Create a dictionary of Cell objects, where the dictionary key is a tuple of the row and column, and
        the value is the Cell object.
        """
        for row in range(self.height):
            for col in range(self.width):
                cell = Cell(row, col)
                self.cells[(row, col)] = cell

    def configure_cells(self):
        """
        For each cell in the grid, set the neighbors of that cell to the cells that are adjacent to it.
        """
        for cell in self.cells.values():
            row = cell.row
            col = cell.column
            cell.neighbors = {
                "north": (row - 1, col),
                "south": (row + 1, col),
                "west": (row, col - 1),
                "east": (row, col + 1),
            }

    def get_cell(self, cell):
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

    def get_neighbors(self, cell, adjacent=True):
        """
        Given a cell, return a list of its neighboring cells

        :param cell: the cell to get the neighbors of
        :param adjacent: ignore diagonal neighbors
        :return: A list of the neighbors of the cell.
        """
        neighbor_coords = [c for c in cell.neighbors.values()]
        neighbors = [self.get_cell(coord) for coord in neighbor_coords if self.get_cell(coord)]
        return neighbors

    def random_cell(self):
        """
        Return a random cell from the grid.
        :return: A random cell from the list of cells.
        """
        cell = random.choice([cell for cell in self.cells.values() if cell])
        return cell

    def size(self):
        """
        Return the number of cells in the grid.
        :return: Number of cells in the grid
        """
        return self.height * self.width

    def each_row(self, bottom_up=False):
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

    def each_cell(self):
        """
        Return a generator that yields a cell at a time.
        """
        for row in range(self.height):
            for col in range(self.width):
                yield self.cells[(row, col)]

    def get_visual_grid(self):
        """
        Create a grid of the maze, with a wall character between each cell.
        :return: A list of lists of strings.
        """
        self.visual_grid = []
        wall = chr(9608)
        for row in self.each_row():
            term_row = []
            lower_row = []
            for i, cell in enumerate(row):
                if cell.get_links():
                    term_row.append(" ")
                else:
                    term_row.append(wall)
                cell_east_coord = cell.neighbors["east"]
                cell_south_coord = cell.neighbors["south"]
                if self.get_cell(cell_east_coord):
                    if cell.is_linked(self.get_cell(cell_east_coord)):
                        term_row.append(" ")
                    else:
                        term_row.append(wall)
                if self.get_cell(cell_south_coord):
                    if cell.is_linked(self.get_cell(cell_south_coord)):
                        lower_row.append(" ")
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

    def __str__(self):
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
                    east_boundary = " "
                else:
                    east_boundary = "|"
                top += body + east_boundary
                if cell.is_linked(self.get_cell(cell.neighbors["south"])):
                    south_boundary = "   "
                else:
                    south_boundary = "---"
                corner = "+"
                bottom += south_boundary + corner

            output += top + "\n"
            output += bottom + "\n"

        return output
