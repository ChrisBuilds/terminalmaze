import random
from collections.abc import Generator
from typing import Optional

from terminalmaze.config import MAZE_THEME
from terminalmaze.resources.cell import Cell
from terminalmaze.visual.visualmaze import Visual


class Grid:
    def __init__(
        self,
        width: int,
        height: int,
        theme: MAZE_THEME,
        mask_string: str | None = None,
    ) -> None:
        """
        Create a new grid with the given width and height.

        :param width: the number of columns in the grid
        :param height: the number of rows in the grid
        :param mask_string: mask to apply
        """
        self.width: int = width
        self.height: int = height
        self.cells: dict[tuple[int, int], Cell] = {}
        self.masked_cells: dict[tuple[int, int], Cell] = {}
        self.unmasked_cells: dict[tuple[int, int], Cell] = {}
        self.prepare_grid()
        self.mask_lines: Optional[list[str]] = self.format_mask(mask_string)
        self.mask_cells()
        self.configure_cells()
        self.visual = Visual(self, theme)
        self.seed: Optional[int] = None

    def format_mask(self, mask_string: Optional[str]) -> Optional[list[str]]:
        """Format the mask string for use in other methods."""
        if not mask_string:
            return None
        mask_lines = []
        for line in mask_string.split("\n"):
            if line.strip().startswith("m:"):
                line = line.strip("m:").strip("\n")
                mask_lines.append(line)
        if not mask_lines:
            return None
        mask_width = len(max(mask_lines, key=len))
        mask_height = len(mask_lines)
        if mask_width > self.width or mask_height > self.height:
            return None
        else:
            return mask_lines

    def prepare_grid(self) -> None:
        """
        Create a dictionary of Cell objects, where the dictionary key is a tuple of the row and column, and
        the value is the Cell object.
        """
        for row in range(self.height):
            for col in range(self.width):
                cell = Cell(row, col)
                self.cells[(row, col)] = cell
                self.unmasked_cells[(row, col)] = cell

    def mask_cells(self) -> None:
        """Translate mask string to cell coordinates centered in the grid. Track masked cells in self.masked_cells
        and unmasked cells in self.unmasked_cells."""

        if not self.mask_lines:
            return
        mask_midpoint_x = -(-len(max(self.mask_lines, key=len)) // 2)
        mask_midpoint_y = -(-len(self.mask_lines) // 2)
        grid_midpoint_x = -(-self.width // 2)
        grid_midpoint_y = -(-self.height // 2)
        x_delta = grid_midpoint_x - mask_midpoint_x
        y_delta = grid_midpoint_y - mask_midpoint_y
        for y, line in enumerate(self.mask_lines):
            for x, symbol in enumerate(line):
                if symbol == "#":
                    cell_coordinates = (y + y_delta, x + x_delta)
                    cell = self.get_cell(cell_coordinates)
                    if cell:
                        self.masked_cells[cell_coordinates] = cell
                    self.unmasked_cells.pop(cell_coordinates, None)

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
                else:
                    cell.neighbors[direction] = None

    def get_cell(self, cell: tuple[int, int]) -> Optional[Cell]:
        """
        Given cell coordinates, return the cell object if valid coordinates, else None.

        :param cell: a tuple of the form (row, column)
        :return: The cell object
        """

        if cell in self.cells:
            return self.cells[cell]
        else:
            return None

    def get_neighbors(self, cell: Cell, ignore_mask=False, existing_only: bool = True) -> dict[str, Optional[Cell]]:
        """
        Given a cell, return a list of its neighboring cells.

        :param cell: the cell to get the neighbors of
        :param ignore_mask: return masked and unmasked neighbors. Defaults to False.
        :param existing_only: if True, only return direction:Cell pair if neighbor exists. Defaults to True.
        :return: A dict of {str,Cell} neighbors.
        """
        neighbors = {}
        for direction, neighbor in cell.neighbors.items():
            if existing_only and not neighbor:
                continue
            neighbors[direction] = neighbor
        if not ignore_mask:
            unmasked_neighbors = {}
            for direction, neighbor in neighbors.items():
                if neighbor not in self.masked_cells.values():
                    unmasked_neighbors[direction] = neighbor
            neighbors = unmasked_neighbors

        return neighbors

    def link_cells(self, cell_a: Cell, cell_b: Cell, bidi: bool = True) -> None:
        """
        Link cells and update visual grid to show link.

        :param cell_a: cell from which the link starts
        :param cell_b: cell to which the link occurs
        :param bidi: If True, the link is bidirectional, defaults to True (optional)
        """
        cell_a.link(cell_b, bidi=bidi)
        self.visual.modify_link_state(cell_a, cell_b)

    def unlink_cells(self, cell_a: Cell, cell_b: Cell, bidi: bool = True) -> None:
        cell_a.unlink(cell_b, bidi=bidi)
        self.visual.modify_link_state(cell_a, cell_b, unlink=True)

    def random_cell(self, ignore_mask: bool = False) -> Cell:
        """Return a random cell from the grid.

        Args:
            ignore_mask (bool, optional): If True, select from all cells, including masked. Defaults to False.

        Returns:
            Cell: Cell
        """
        if ignore_mask:
            cell = random.choice(list(self.cells.values()))
        else:
            cell = random.choice(list(self.unmasked_cells.values()))
        return cell

    def size(self) -> int:
        """
        Return the number of cells in the grid.
        :return: Number of cells in the grid
        """
        return self.height * self.width

    def each_row(self, ignore_mask: bool = False, bottom_up: bool = False) -> Generator[list[Cell], None, None]:
        """
        Yield one row of the grid at a time as a list.

        :param ignore_mask: If True, include masked cells in the list of cells, defaults to False (optional)
        :param bottom_up: If True, the cells are traversed in bottom-up order, defaults to False (optional)
        """
        if bottom_up:
            range_gen = range(self.height - 1, -1, -1)
        else:
            range_gen = range(self.height)
        for row in range_gen:
            if ignore_mask:
                yield [self.cells[(row, col)] for col in range(self.width)]
            else:
                yield [
                    unmasked_cell
                    for col in range(self.width)
                    if (unmasked_cell := self.unmasked_cells.get((row, col), None))
                ]

    def each_column(self, ignore_mask: bool = False) -> Generator[list[Cell], None, None]:
        """
        Yield one column of the grid at a time as a list.

        :param ignore_mask: If True, include masked cells in the list of cells, defaults to False (optional)
        """
        for column in range(self.width):
            if ignore_mask:
                yield [self.cells[(row, column)] for row in range(self.height)]

    def each_cell(self, ignore_mask: bool = False) -> Generator[Cell, None, None]:
        """
        Return a generator that yields a cell at a time.
        :param ignore_mask: If True, include masked cells, defaults to False (optional)
        """
        for row in range(self.height):
            for col in range(self.width):
                if ignore_mask:
                    yield self.cells[(row, col)]
                else:
                    cell = self.unmasked_cells.get((row, col), None)
                    if cell:
                        yield cell
