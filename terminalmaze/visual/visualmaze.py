import random
import time
from os import get_terminal_size, system

import terminalmaze.visual.colorterm as colorterm
import terminalmaze.visual.visualeffects as ve
from terminalmaze.config import MAZE_THEME, tm_config
from terminalmaze.resources.cell import Cell


class Visual:
    """Visual representation of the maze graph and operations on the visual."""

    def __init__(self, grid, theme: MAZE_THEME):
        """Prepare a visual representation of the maze graph.

        Parameters
        ----------
        theme : theme class from terminalmaze.config
        grid : terminalmaze.resources.grid.Grid

        Returns
        -------
        None
        """
        self.grid = grid
        self.theme = theme
        self.wall = f"{colorterm.fg(theme.wall.color)}{theme.wall.character}{colorterm.RESET}"
        self.path = f"{colorterm.fg(theme.path.color)}{theme.path.character}{colorterm.RESET}"
        self.group_color_pool = list(range(0, 256))
        self.group_color_map: dict[int, int] = dict()
        self.last_groups: ve.GroupType
        self.visual_grid: list[list[str]] = list()
        self.passages: set[tuple[int, int]] = set()
        self.last_show_time = time.time()
        self.start_time = time.time()
        self.terminal_width = self.get_terminal_width()
        self.prepare_visual()

    @staticmethod
    def get_terminal_width() -> int:
        """
        Get the terminal size using os.get_terminal_size(). If unable to get terminal size, return 0.
        Returns
        -------
        int : Column width of terminal, or 0 if unable to retrieve terminal size
        """
        try:
            columns, lines = get_terminal_size()
            return columns
        except OSError:
            return 0

    @staticmethod
    def translate_cell_coords(cell: Cell) -> tuple[int, int]:
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

    def get_group_color(self, group_id: int) -> str:
        """If the group id has an assigned color, return the assigned color, else get a random
        color from the color pool, assign it to the group, and return the color int.

        Args:
            group_id (int): id for cell group

        Returns:
            str: colorterm.fg() color string
        """
        color = self.group_color_map.get(group_id)
        if color:
            return colorterm.fg(color)

        color = self.group_color_pool.pop(random.randint(0, len(self.group_color_pool) - 1))
        self.group_color_map[group_id] = color

        if not self.group_color_pool:
            self.group_color_pool = list(range(0, 256))

        return colorterm.fg(self.group_color_map[group_id])

    def modify_link_state(self, cell_a: Cell, cell_b: Cell, unlink=False) -> None:
        """Replace characters for linked cells and the wall between them.

        Parameters
        ----------
        cell_a : Cell being (un)linked from
        cell_b : Cell being (un)linked to
        unlink : bool
        """
        character = self.path
        if unlink:
            character = self.wall

        # replace character on cells with wall/path for (un)linked cells
        for cell in (cell_a, cell_b):
            row, column = self.translate_cell_coords(cell)
            if not cell.links:
                self.visual_grid[row][column] = self.wall
            else:
                self.visual_grid[row][column] = self.path

        # replace character between cells
        offsets = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}
        for direction, offset in offsets.items():
            row_offset, column_offset = offset
            row, column = self.translate_cell_coords(cell_a)

            if cell_b is cell_a.neighbors[direction]:
                self.visual_grid[row + row_offset][column + column_offset] = character
                if unlink:
                    self.passages.discard((row + row_offset, column + column_offset))
                else:
                    self.passages.add((row + row_offset, column + column_offset))
                return

    def add_visual_effects(self, visual_effects: dict[str, ve.VisualEffect], verbosity: int) -> list[list[str]]:
        """Apply color to cells and passages to show logic.

        Args:
            visual_effects (dict[str, ve.VisualEffect]): Effects for cells to be colorterm
            verbosity : Determines which effects are applied

        Returns:
            list[list[str]]: visual grid with colorterm cells
        """
        colored_visual_grid = [line.copy() for line in self.visual_grid]
        pending_effects = sorted(visual_effects.values())
        while pending_effects:
            current_effect = pending_effects.pop(0)
            if verbosity not in current_effect.verbosity:
                continue

            if isinstance(current_effect, ve.ModifySingleCell):
                colored_visual_grid = self.color_single_cell(colored_visual_grid, current_effect)

            elif isinstance(current_effect, ve.ModifyMultipleCells):
                colored_visual_grid = self.color_multiple_cells(colored_visual_grid, current_effect)

            elif isinstance(current_effect, ve.RandomColorGroup):
                if current_effect.groups:
                    self.last_groups = current_effect.groups
                    colored_visual_grid = self.color_cell_groups(colored_visual_grid, current_effect)

            elif isinstance(current_effect, ve.Animation):
                colored_visual_grid = self.animate_cells(colored_visual_grid, current_effect)

        return colored_visual_grid

    def animate_cells(self, colored_visual_grid: list[list[str]], visual_effect: ve.Animation) -> list[list[str]]:
        def get_value_at_modification_index(i, collection):
            if i < len(collection):
                return collection[i]
            return None

        color = character = None
        translated_cells = set()
        for cell in visual_effect.cells:
            if cell:
                translated_cells.add(self.translate_cell_coords(cell))

        visual_effect.cells.clear()
        cells_and_passages = self.find_passages(translated_cells | visual_effect.animating.keys())
        for key in visual_effect.animating.keys():
            cells_and_passages.discard(key)

        visual_effect.animating |= {
            visual_coordinates: [0, visual_effect.frames_per_value] for visual_coordinates in cells_and_passages
        }
        transition_complete = []
        for visual_coordinate, transition_details in visual_effect.animating.items():
            modification_index, frames_until_transition = transition_details
            if frames_until_transition:
                visual_effect.animating[visual_coordinate][1] -= 1
                color = get_value_at_modification_index(modification_index, visual_effect.colors)
                character = get_value_at_modification_index(modification_index, visual_effect.characters)

            if not visual_effect.animating[visual_coordinate][1]:
                visual_effect.animating[visual_coordinate][0] += 1
                visual_effect.animating[visual_coordinate][1] = visual_effect.frames_per_value

            if visual_effect.animating[visual_coordinate][0] >= len(visual_effect.colors) and visual_effect.animating[
                visual_coordinate
            ][0] >= len(visual_effect.characters):
                transition_complete.append(visual_coordinate)

            if character and len(character) > 1:
                character = random.choice(character)
            if color and isinstance(color, list):
                color = random.choice(color)
            if character or color:
                if color:
                    color = colorterm.fg(color)
                colored_visual_grid = self.apply_cell_modification(
                    colored_visual_grid, visual_coordinate, character=character, color=color
                )
        for visual_coordinate in transition_complete:
            del visual_effect.animating[visual_coordinate]
        return colored_visual_grid

    def color_multiple_cells(
        self, colored_visual_grid: list[list[str]], visual_effect: ve.ModifyMultipleCells
    ) -> list[list[str]]:
        """Color multiple cells the same color.

        Args:
            colored_visual_grid (list[list[str]]): List of cells to be colorterm.
            visual_effect (ve.Multiple): Dataclass

        Returns:
            list[list[str]]: colorterm visual grid.
        """
        if not visual_effect.cells:
            return colored_visual_grid
        translated_cells = set(self.translate_cell_coords(cell) for cell in visual_effect.cells)
        cells_and_passages = self.find_passages(translated_cells)
        color_str = colorterm.fg(visual_effect.color)
        for visual_coordinates in cells_and_passages:
            colored_visual_grid = self.apply_cell_modification(colored_visual_grid, visual_coordinates, color_str)
        return colored_visual_grid

    def color_single_cell(
        self, colored_visual_grid: list[list[str]], visual_effect: ve.ModifySingleCell
    ) -> list[list[str]]:
        """Color a single cell the given color.

        Args:
            colored_visual_grid (list[list[str]]): Copy of visual_grid.
            visual_effect (ve.Single): Dataclass for visual effects.

        Raises:
            ValueError: color int must be 0 <= color <= 256

        Returns:
            list[list[str]]: colorterm visual grid
        """
        if not visual_effect.cell:
            return colored_visual_grid

        visual_coordinates = self.translate_cell_coords(visual_effect.cell)
        if 0 <= visual_effect.color <= 256:
            color_str = colorterm.fg(visual_effect.color)
            colored_visual_grid = self.apply_cell_modification(colored_visual_grid, visual_coordinates, color_str)
        else:
            raise ValueError(f"visual_effect.color value: {visual_effect.color} not in valid range (0 - 256)")
        return colored_visual_grid

    def color_cell_groups(
        self, colored_visual_grid: list[list[str]], visual_effect: ve.RandomColorGroup | None
    ) -> list[list[str]]:
        """Color cell groups.

        Args: colored_visual_grid (list[list[str]]): Copy of visual_grid. visual_effect (Optional[
        ve.RandomColorGroup], optional): Dict mapping group ID's to lists of cells. Defaults to None.

        Returns:
            list[list[str]]: colorterm visual grid
        """
        groups = None
        if visual_effect and visual_effect.groups:
            groups = visual_effect.groups

        elif self.last_groups:
            groups = self.last_groups

        if groups:
            for group, cells in self.last_groups.items():
                group_color = self.get_group_color(group)
                translated_cells = set(self.translate_cell_coords(cell) for cell in cells)
                cells_and_passages = self.find_passages(translated_cells)
                for visual_coordinates in cells_and_passages:
                    colored_visual_grid = self.apply_cell_modification(
                        colored_visual_grid, visual_coordinates, group_color
                    )
        return colored_visual_grid

    def find_passages(self, translated_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        """Identify passages between linked cells.

        Args:
            translated_cells (set[tuple[int, int]]): Visual coordinates for cells

        Returns:
            set[tuple[int, int]]: translated cells with passages added
        """
        for visual_coordinates in self.passages:
            visual_y, visual_x = visual_coordinates
            if ((visual_y + 1, visual_x) in translated_cells and (visual_y - 1, visual_x) in translated_cells) or (
                (visual_y, visual_x + 1) in translated_cells and (visual_y, visual_x - 1) in translated_cells
            ):
                translated_cells.add(visual_coordinates)
        return translated_cells

    def apply_cell_modification(
        self,
        colored_visual_grid: list[list[str]],
        visual_coordinates: tuple[int, int],
        color: str | None = None,
        character: str | None = None,
    ) -> list[list[str]]:

        y, x = visual_coordinates
        current_character = colored_visual_grid[y][x].replace(colorterm.RESET, "")[-1]
        current_color = colored_visual_grid[y][x].replace(colorterm.RESET, "")[:-1]
        if character:
            current_character = character
        if color:
            current_color = color
        colored_visual_grid[y][
            x
        ] = f"{colorterm.bg(self.theme.wall.color)}{current_color}{current_character}{colorterm.RESET}"
        return colored_visual_grid

    def format_status(self, status_text: dict[str, str | int | None]) -> str:
        """
        Create a status string from the status_text dict.

        Parameters
        ----------
        status_text : dict of label:value pairs for status updates

        Returns
        -------
        str : status string
        """
        status_string = ""
        for label, value in status_text.items():
            status_string += f" {label}: {value} |"
        status_string = status_string.strip("|").strip()
        if self.terminal_width:
            status_string = status_string + (" " * (self.terminal_width - len(status_string)))
        return status_string

    def time_elapsed(self) -> str:
        """
        Calculate the run time in minutes/seconds and return string representation.
        Returns
        -------
        str : Time in format {minutes}m {seconds}s
        """
        seconds = time.time() - self.start_time
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}m {seconds}s"

    def show(
        self,
        visual_effects: dict[str, ve.VisualEffect],
        status_text: dict[str, str | int | None],
        verbosity: int,
        complete: bool = False,
        nostatus: bool = False,
    ) -> None:
        """

        Parameters
        ----------
        nostatus :
        visual_effects : Effects to be applied to the maze
        status_text : Status texts to display below the maze
        verbosity : Determines which visual effects are shown
        complete : Indicates the maze is complete, final image of the maze

        Returns
        -------

        """
        terminal_delay = tm_config["global"]["terminal_delay"]

        if verbosity == 0:
            print(self.format_status(status_text), end="\r")
            if not complete:
                return

        maze_visual = self.add_visual_effects(visual_effects, verbosity)
        lines = ["".join(line) for line in maze_visual]
        time_since_last_show = time.time() - self.last_show_time
        if time_since_last_show < terminal_delay:
            time.sleep(terminal_delay - time_since_last_show)
        status_text["Time Elapsed"] = self.time_elapsed()
        system("clear")
        print("\n".join(lines))
        if not nostatus:
            print(f"{colorterm.RESET}{self.format_status(status_text)}")
        self.last_show_time = time.time()
