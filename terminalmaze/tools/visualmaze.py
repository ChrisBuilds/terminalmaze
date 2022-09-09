from collections import defaultdict
from terminalmaze.resources.cell import Cell
from dataclasses import dataclass
import colored
import random
from os import system
from typing import Union, DefaultDict, Optional


class Visual:
    """Visual representation of the maze graph and operations on the visual."""

    @dataclass
    class VisualEffect:
        """Simple dataclass for organizing visual effect data for use in the maze visual."""

        style: str
        cells: Union[Cell, list[Cell], dict[int, list[Cell]]]

    def __init__(self, grid) -> None:
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
        self.group_color_map: dict[int, Union[int, str]] = dict()
        self.last_groups: Union[dict[int, list[Cell]], dict[int, set[Cell]], dict] = dict()
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

    def get_group_color(self, group_id: int) -> Union[int, str]:
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

    def add_logic_data(
        self,
        logic_data: dict[
            str, Union[Cell, list[Cell], dict[int, Cell], DefaultDict[int, list[Cell]], DefaultDict[int, set[Cell]]]
        ],
    ) -> list[list[str]]:
        """Apply color to cells and walls to show logic.

        Args:
            logic_data (dict[str, Union[list[Cell], Cell, dict[int, list[Cell]]]]): label : cell pairs for various logical
            indicators.

        Returns:
            list[list[str]]: visual grid with colored cells
        """
        colored_visual_grid = [line.copy() for line in self.visual_grid]
        if not logic_data.get("groups", None):
            self.color_cell_groups(colored_visual_grid)

        for label, data in logic_data.items():
            if isinstance(data, list):
                translated_cells = set(self.translate_cell_coords(cell) for cell in data)
                cells_and_passages = self.find_passages(translated_cells)
                for visual_coordinates in cells_and_passages:
                    self.apply_color(colored_visual_grid, visual_coordinates, self.color_map[label])

            elif label == "groups" and isinstance(data, dict) or isinstance(data, defaultdict):
                self.last_groups = data
                self.color_cell_groups(colored_visual_grid)

            elif isinstance(data, Cell):
                visual_coordinates = self.translate_cell_coords(data)
                self.apply_color(colored_visual_grid, visual_coordinates, self.color_map[label])
            else:
                raise Exception(
                    f"Invalid type for 'data' in 'logic_data', \
                should be dict[str, Union[set[Cell], Cell, dict[int, set[Cell]]]]\ndata = {data}"
                )

        return colored_visual_grid

    def color_cell_groups(self, colored_visual_grid: list[list[str]]) -> None:
        """Apply color to groups of cells.

        Args:
            colored_visual_grid (list[list[str]]): copy of self.visual_grid
        """
        if self.last_groups:
            for group, cells in self.last_groups.items():
                group_color = self.get_group_color(group)
                translated_cells = set(self.translate_cell_coords(cell) for cell in cells)
                cells_and_passages = self.find_passages(translated_cells)
                for visual_coordinates in cells_and_passages:
                    self.apply_color(colored_visual_grid, visual_coordinates, str(group_color))

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
        visual_effects: dict[
            str, Union[Cell, list[Cell], dict[int, Cell], DefaultDict[int, list[Cell]], DefaultDict[int, set[Cell]]]
        ],
        status_text: dict[str, Union[Optional[str], Optional[int]]],
        showlogic: bool = False,
    ):
        """Apply coloring based on logic data if showlogic, then print the maze.

        Args:
            logic_data (dict[str, Union[Cell, list[Cell], dict[int, set[Cell]]]]): cell pairs for various logical
            indicators.
            showlogic (bool, optional): Apply coloring based on logic if True, else skip coloring. Defaults to False.
        """
        if showlogic:
            maze_visual = self.add_logic_data(visual_effects)
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
