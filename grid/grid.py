from grid.cell import Cell
import random
import colored
from os import system
from collections.abc import Generator
from typing import Optional, Union


class Grid:
    def __init__(self, width: int = 20, height: int = 10, mask: Optional[list[str]] = None) -> None:
        """
        Create a new grid with the given width and height.

        :param width: the number of columns in the grid
        :param height: the number of rows in the grid
        :param mask: mask to apply
        """
        self.width: int = width
        self.height: int = height
        self.mask: list[str] = mask
        self.cells: dict[tuple[int, int], Cell] = {}
        self.masked_cells: dict[tuple[int, int], Cell] = {}
        self.unmasked_cells: dict[tuple[int, int], Cell] = {}
        if self.mask:
            self.format_mask()
        self.prepare_grid()
        self.configure_cells()
        self.wall = f"{colored.fg(240)}{chr(9608)}"
        self.path = f"{colored.fg(6)}{chr(9608)}"  # 29
        self.visual = Visual(self)
        self.seed: int = None

    def format_mask(self) -> None:
        """Format the mask string for use in other methods."""
        mask_lines = []
        for line in self.mask.split("\n"):
            if line.strip().startswith("m:"):
                line = line.strip("m:").strip("\n")
                mask_lines.append(line)
        self.mask = mask_lines
        mask_width = len(max(self.mask, key=len))
        mask_height = len(self.mask)
        if mask_width > self.width or mask_height > self.height:
            self.mask = None

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

        if self.mask:
            self.mask_cells()

    def mask_cells(self) -> None:
        """Translate mask string to cell coordinates centered in the grid. Track masked cells in self.masked_cells
        and unmasked cells in self.unmasked_cells."""
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
        row = cell[0]
        column = cell[1]
        if cell in self.cells:
            return self.cells[cell]
        else:
            return None

    def get_neighbors(
        self, cell: Cell, ignore_mask=False, existing_only: bool = True, adjacent: bool = True
    ) -> dict[str, Cell]:
        """
        Given a cell, return a list of its neighboring cells.

        :param cell: the cell to get the neighbors of
        :param ignore_mask: return masked and unmasked neighbors. Defaults to False.
        :param existing_only: if True, only return direction:Cell pair if neighbor exists. Defaults to True.
        :param adjacent: ignore diagonal neighbors. Defaults to True
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
        self.visual.link_cells(cell_a, cell_b)

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
        if not bottom_up:
            for row in range(self.height):
                if ignore_mask:
                    yield [self.cells[(row, col)] for col in range(self.width)]
                else:
                    yield [
                        self.unmasked_cells.get((row, col), None)
                        for col in range(self.width)
                        if self.unmasked_cells.get((row, col), None)
                    ]
        else:
            for row in range(self.height - 1, -1, -1):
                if ignore_mask:
                    yield [self.cells[(row, col)] for col in range(self.width)]
                else:
                    yield [
                        self.unmasked_cells.get((row, col), None)
                        for col in range(self.width)
                        if self.unmasked_cells.get((row, col), None)
                    ]

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


class Visual:
    """Visual representation of the maze graph and operations on the visual."""

    def __init__(self, grid: Grid) -> None:
        """Prepare a visual representation of the maze graph.

        Args:
            grid (Grid): Maze
        """
        self.grid = grid
        self.wall = f"{colored.fg(240)}{chr(9608)}"
        self.path = f"{colored.fg(6)}{chr(9608)}"  # 29
        self.color_map = {
            "working_cell": colored.fg(45),
            "last_linked": colored.fg(218),
            "invalid_neighbors": colored.fg(52),
            "frontier": colored.fg(231),
            "explored": colored.fg(218),  # 137
            "position": colored.fg(76),
            "target": colored.fg(202),
            "start": colored.fg(211),
            "path": colored.fg(218),  # 133
            "logic0": colored.fg(237),
            "logic1": colored.fg(28),
            "groups": None,
        }
        self.group_color_pool = list(range(1, 256))
        self.group_color_map: dict[int, int] = dict()
        self.visual_grid: list[list[str]] = list()
        self.visual_links: set[tuple[int, int]] = set()
        self.prepare_visual()

    def prepare_visual(self) -> None:
        """Prepare a visual representation of the maze graph."""
        for row in self.grid.each_row(ignore_mask=True):
            term_row = []
            lower_row = []
            for i, cell in enumerate(row):
                term_row.append(self.wall)
                cell_east = cell.neighbors.get("east")
                cell_south = cell.neighbors.get("south")
                if cell_east:
                    term_row.append(self.wall)
                if cell_south:
                    lower_row.append(self.wall)
                if i != len(row) - 1:
                    lower_row.append(self.wall)
            self.visual_grid.append(term_row)
            self.visual_grid.append(lower_row)
        self.visual_grid.pop(-1)  # remove extra lower row
        for row in self.visual_grid:
            row.insert(0, self.wall)
            row.append(self.wall)
        self.visual_grid.insert(0, [self.wall for _ in range(len(self.visual_grid[0]))])
        self.visual_grid.append([self.wall for _ in range(len(self.visual_grid[0]))])

    def get_group_color(self, group_id: int) -> int:
        """If the group id has an assigned color, return the assigned color, else get a random
        color from the color pool, assign it to the group, and return the color int.

        Args:
            group_id (int): id for cell group

        Returns:
            int: colored color int
        """
        color = self.group_color_map.get(group_id)
        if color:
            return color
        color = self.group_color_pool.pop(random.randint(0, len(self.group_color_pool) - 1))
        self.group_color_map[group_id] = colored.fg(color)
        if not self.group_color_pool:
            self.group_color_pool = list(range(1, 256))
        return self.group_color_map[group_id]

    def translate_cell_coords(self, cell: Cell) -> tuple[int, int]:
        """Translate cell coordinates to match row, column indexes in the visual
        grid.

        :param cell: cell to translate
        :return: ruple (row, column)
        """
        row = cell.row
        column = cell.column
        if row == 0:
            row = 1
        else:
            row = (row * 2) + 1
        if column == 0:
            column = 1
        else:
            column = (column * 2) + 1
        return row, column

    def link_cells(self, cell_a: Cell, cell_b: Cell) -> None:
        """Replace characters for linked cells and the wall between them.

        Args:
            cell_a (Cell): Cell being linked from
            cell_b (Cell): Cell being linked to
        """
        # replace wall on cells with path for linked cells
        for cell in (cell_a, cell_b):
            row, column = self.translate_cell_coords(cell)
            self.visual_grid[row][column] = self.path

        # replace wall between cells with path
        offsets = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}
        for direction, offset in offsets.items():
            row_offset, column_offset = offset
            row, column = self.translate_cell_coords(cell_a)
            if cell_b is cell_a.neighbors[direction]:
                self.visual_grid[row + row_offset][column + column_offset] = self.path
                self.visual_links.add((row + row_offset, column + column_offset))
                return

    def add_logic_data(self, logic_data: dict[str, Union[list[Cell], Cell, dict[int, list[Cell]]]]) -> list[list[str]]:
        """Apply color to cells and walls to show logic.

        Args:
            logic_data (dict[str, Union[list[Cell], Cell, dict[int, list[Cell]]]]): label : cell pairs for various logical
            indicators.

        Returns:
            list[list[str]]: visual grid with colored cells
        """
        colored_visual_grid = [line.copy() for line in self.visual_grid]
        for label, data in logic_data.items():
            if isinstance(data, list):
                translated_cells = set(self.translate_cell_coords(cell) for cell in data)
                cells_and_passages = self.find_passages(translated_cells)
                for visual_coordinates in cells_and_passages:
                    self.apply_color(colored_visual_grid, visual_coordinates, self.color_map[label])

            elif isinstance(data, dict):
                for group, cells in data.items():
                    group_color = self.get_group_color(group)
                    translated_cells = set(self.translate_cell_coords(cell) for cell in cells)
                    cells_and_passages = self.find_passages(translated_cells)
                    for visual_coordinates in cells_and_passages:
                        self.apply_color(colored_visual_grid, visual_coordinates, group_color)

            else:
                visual_coordinates = self.translate_cell_coords(data)
                self.apply_color(colored_visual_grid, visual_coordinates, self.color_map[label])
        return colored_visual_grid

    def find_passages(self, translated_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        """Identify passages between linked cells.

        Args:
            translated_cells (set[tuple[int, int]]): Visual coordinates for cells

        Returns:
            set[tuple[int, int]]: translated cells with passages added
        """
        for visual_coordinates in self.visual_links:
            visual_y, visual_x = visual_coordinates
            if ((visual_y + 1, visual_x) in translated_cells and (visual_y - 1, visual_x) in translated_cells) or (
                (visual_y, visual_x + 1) in translated_cells and (visual_y, visual_x - 1) in translated_cells
            ):
                translated_cells.add(visual_coordinates)
        return translated_cells

    def apply_color(
        self, colored_visual_grid: list[list[str]], visual_coordinates: tuple[int, int], color: str
    ) -> None:
        """Apply the given color to the character at the given coordinates.

        Args:
            colored_visual_grid (list[list[str]]): visual grid copy used for logic coloring
            visual_coordinates (tuple[int, int]): row,column coordinates of the character to be colored
            color (str): colored.fg() color to apply to the character
        """
        y, x = visual_coordinates
        colored_visual_grid[y][x] = f"{color}{chr(9608)}"

    def show(
        self,
        logic_data: dict[str, Union[list[Cell], Cell]],
        status_text: dict[str, Union[str, int]],
        showlogic: bool = False,
    ):
        """Apply coloring based on logic data if showlogic, then print the maze.

        Args:
            logic_data (dict[str, Union[list[Cell], Cell]]): cell pairs for various logical
            indicators.
            showlogic (bool, optional): Apply coloring based on logic if True, else skip coloring. Defaults to False.
        """
        if showlogic:
            maze_visual = self.add_logic_data(logic_data)
        else:
            maze_visual = self.visual_grid
        lines = ["".join(line) for line in maze_visual]
        status_string = ""
        for label, value in status_text.items():
            status_string += f" {label}: {value} |"
        status_string = status_string.strip("|").strip()
        system("clear")
        print("\n".join(lines))
        print(status_string)
