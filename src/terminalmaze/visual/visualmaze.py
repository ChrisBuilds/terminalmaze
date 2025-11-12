import random
import shutil
import sys
import time
from collections import defaultdict
from types import SimpleNamespace

import terminalmaze.visual.colorterm as colorterm
import terminalmaze.visual.visualeffects as ve
from terminalmaze.config import MAZE_THEME
from terminalmaze.resources.cell import Cell
from terminalmaze.visual import ansitools


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
        self.passage_map: defaultdict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
        self.last_show_time = time.time()
        self.start_time = time.time()
        self.terminal_width, self.terminal_height = self._get_terminal_dimensions()
        self.prepare_visual()
        self.prep_terminal()

    def prep_terminal(self) -> None:
        sys.stdout.write(ansitools.HIDE_CURSOR())
        print("\n" * (len(self.visual_grid) + 2))
        sys.stdout.write(ansitools.DEC_SAVE_CURSOR_POSITION())

    def _get_terminal_dimensions(self) -> tuple[int, int]:
        """Gets the terminal dimensions.

        Returns:
            tuple[int, int]: terminal width and height
        """
        try:
            terminal_width, terminal_height = shutil.get_terminal_size()
        except OSError:
            # If the terminal size cannot be determined, return default values
            return 80, 24
        return terminal_width, terminal_height

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
        cell_a_translated = self.translate_cell_coords(cell_a)
        cell_b_translated = self.translate_cell_coords(cell_b)
        for cell, visual_coordinates in {
            cell_a: cell_a_translated,
            cell_b: cell_b_translated,
        }.items():
            row, column = visual_coordinates
            if not cell.links:
                self.visual_grid[row][column] = self.wall
            else:
                self.visual_grid[row][column] = self.path

        # replace character between cells
        offsets = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}
        for direction, offset in offsets.items():
            row_offset, column_offset = offset
            cell_row, cell_column = cell_a_translated

            if cell_b is cell_a.neighbors[direction]:
                passage_row = cell_row + row_offset
                passage_column = cell_column + column_offset
                self.visual_grid[passage_row][passage_column] = character
                if unlink:
                    self.passage_map[cell_a_translated].discard((passage_row, passage_column))
                    self.passage_map[cell_b_translated].discard((passage_row, passage_column))
                    self.passages.discard((passage_row, passage_column))
                else:
                    self.passage_map[(cell_row, cell_column)].add((passage_row, passage_column))
                    self.passages.add((passage_row, passage_column))
                return

    def add_visual_effects(self, visual_effects: dict[str, ve.VisualEffect], verbosity: int) -> list[list[str]]:
        """Apply color to cells and passage_map to show logic.

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
                    colored_visual_grid = self.color_cell_groups(colored_visual_grid)

            elif isinstance(current_effect, ve.Animation):
                colored_visual_grid = self.animate_cells(colored_visual_grid, current_effect)

        return colored_visual_grid

    def animate_cells(self, colored_visual_grid: list[list[str]], visual_effect: ve.Animation) -> list[list[str]]:
        """
        Modify cells in the grid to the character and color specified in the animation visual effect. Track
        cells being animated, including passage_map, and frame position.

        Parameters
        ----------
        colored_visual_grid : List[List[str]] :
        visual_effect : terminalmaze.visual.visualeffects.Animation

        Returns
        -------
        List[List[str]] : Maze grid with color and character changes applied.
        """

        def get_value_at_animation_state_index(state_index: int, collection):
            """
            Get the character, color, and frame duration for a given state_index.

            Parameters
            ----------
            state_index : int
            collection : List[List[str]]

            Returns
            -------
            Tuple[str, str, int]
            """
            if state_index >= len(collection):
                return None, None, 0
            color_value, character_symbol, frame_duration_at_state_index = collection[state_index]
            if isinstance(color_value, list):
                color_value = random.choice(color_value)
            if isinstance(character_symbol, list):
                character_symbol = random.choice(character_symbol)
            if isinstance(frame_duration_at_state_index, list):
                frame_duration_at_state_index = random.choice(frame_duration_at_state_index)
            return color_value, character_symbol, int(frame_duration_at_state_index)

        color = character = None
        translated_cells = set()
        for cell in visual_effect.cells:
            if cell:
                translated_cells.add(self.translate_cell_coords(cell))

        visual_effect.cells.clear()

        cells_and_passages = set()
        cells_to_animate = translated_cells | visual_effect.animating.keys()
        for visual_coordinate in cells_to_animate:
            for passage in self.passage_map.get(visual_coordinate, set()):
                if (
                    len(
                        {
                            (passage[0], passage[1] + 1),
                            (passage[0], passage[1] - 1),
                            (passage[0] + 1, passage[1]),
                            (passage[0] - 1, passage[1]),
                        }
                        & cells_to_animate
                    )
                    == 2
                ):
                    cells_and_passages.add(passage)
        cells_and_passages |= translated_cells
        cells_and_passages -= visual_effect.animating.keys()
        cells_and_passages -= visual_effect.animation_completed_passages

        new_cells_initialization = {}
        for visual_coordinates in cells_and_passages:
            animation_state = SimpleNamespace()
            (
                initial_color,
                initial_character,
                initial_frame_duration,
            ) = get_value_at_animation_state_index(0, visual_effect.animation_details)
            animation_state.animation_state_index = 0
            if isinstance(visual_effect.cycles, list):
                animation_state.cycles_remaining = random.choice(visual_effect.cycles)
            else:
                animation_state.cycles_remaining = visual_effect.cycles - 1
            animation_state.frame_counter = initial_frame_duration
            animation_state.persistent_character = ""
            animation_state.final_state_index = len(visual_effect.animation_details) - 1
            new_cells_initialization[visual_coordinates] = animation_state
        visual_effect.animating |= new_cells_initialization

        animation_complete = []
        for visual_coordinate, animation_state in visual_effect.animating.items():
            if animation_state.frame_counter:
                animation_state.frame_counter -= 1
                color, character, frame_duration = get_value_at_animation_state_index(
                    animation_state.animation_state_index,
                    visual_effect.animation_details,
                )
                if len(character) > 1:
                    if not animation_state.persistent_character:
                        character = random.choice(character)
                        animation_state.persistent_character = character
                    else:
                        character = animation_state.persistent_character

            if animation_state.frame_counter == 0:
                if (
                    animation_state.animation_state_index == animation_state.final_state_index
                    and animation_state.cycles_remaining > 0
                ):
                    animation_state.animation_state_index = 0
                    animation_state.cycles_remaining -= 1

                if animation_state.animation_state_index < animation_state.final_state_index:
                    animation_state.animation_state_index += 1
                    animation_state.frame_counter = get_value_at_animation_state_index(
                        animation_state.animation_state_index,
                        visual_effect.animation_details,
                    )[2]
                else:
                    animation_complete.append(visual_coordinate)
                animation_state.persistent_character = ""

            if character or color:
                if color:
                    color = colorterm.fg(color)
                colored_visual_grid = self.apply_cell_modification(
                    colored_visual_grid,
                    visual_coordinate,
                    character=character,
                    color=color,
                )
                color = character = None
        for visual_coordinate in animation_complete:
            if visual_coordinate in self.passages:
                visual_effect.animation_completed_passages.add(visual_coordinate)
            del visual_effect.animating[visual_coordinate]
        return colored_visual_grid

    def color_multiple_cells(
        self,
        colored_visual_grid: list[list[str]],
        visual_effect: ve.ModifyMultipleCells,
    ) -> list[list[str]]:
        """Color multiple cells the same color.

        Args:
            colored_visual_grid (list[list[str]]): List of cells to be colored.
            visual_effect (ve.Multiple): Dataclass

        Returns:
            list[list[str]]: colorterm visual grid.
        """
        if not visual_effect.cells:
            return colored_visual_grid
        translated_cells = set(self.translate_cell_coords(cell) for cell in visual_effect.cells)
        color_str = colorterm.fg(visual_effect.color)
        for visual_coordinates in translated_cells:
            colored_visual_grid = self.apply_cell_modification(colored_visual_grid, visual_coordinates, color_str)
            for passage in self.passage_map.get(visual_coordinates, set()):
                if (
                    len(
                        {
                            (passage[0], passage[1] + 1),
                            (passage[0], passage[1] - 1),
                            (passage[0] + 1, passage[1]),
                            (passage[0] - 1, passage[1]),
                        }
                        & translated_cells
                    )
                    == 2
                ):
                    colored_visual_grid = self.apply_cell_modification(colored_visual_grid, passage, color_str)
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
        color_str = colorterm.fg(visual_effect.color)
        colored_visual_grid = self.apply_cell_modification(colored_visual_grid, visual_coordinates, color_str)

        return colored_visual_grid

    def color_cell_groups(self, colored_visual_grid: list[list[str]]) -> list[list[str]]:
        """Color cell groups.

        Args: colored_visual_grid (list[list[str]]): Copy of visual_grid. visual_effect (Optional[
        ve.RandomColorGroup], optional): Dict mapping group ID's to lists of cells. Defaults to None.

        Returns:
            list[list[str]]: colorterm visual grid
        """

        for group, cells in self.last_groups.items():
            group_color = self.get_group_color(group)
            translated_cells = set(self.translate_cell_coords(cell) for cell in cells)
            # cells_and_passages = self.find_passages(translated_cells)
            for visual_coordinates in translated_cells:
                colored_visual_grid = self.apply_cell_modification(colored_visual_grid, visual_coordinates, group_color)
                for passage in self.passage_map.get(visual_coordinates, set()):
                    colored_visual_grid = self.apply_cell_modification(colored_visual_grid, passage, group_color)
        return colored_visual_grid

    def apply_cell_modification(
        self,
        colored_visual_grid: list[list[str]],
        visual_coordinates: tuple[int, int],
        color: str | None = None,
        character: str | None = None,
    ) -> list[list[str]]:
        """
        Change the character and/or color of the value at the given visual_coordinate in the colored_visual_grid.

        Parameters
        ----------
        colored_visual_grid : List[List[str]]
        visual_coordinates : Tuple[int, int]
        color : str
        character : str

        Returns
        -------
        List[List[str]]
        """

        y, x = visual_coordinates
        current_character = colored_visual_grid[y][x].replace(colorterm.RESET, "")[-1]
        current_color = colored_visual_grid[y][x].replace(colorterm.RESET, "")[:-1]
        if character:
            current_character = character
        if color:
            current_color = color
        colored_visual_grid[y][x] = (
            f"{colorterm.bg(self.theme.wall.color)}{current_color}{current_character}{colorterm.RESET}"
        )
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
        redrawdelay: float = 0.015,
    ) -> None:
        """

        Parameters
        ----------
        nostatus :
        visual_effects : Effects to be applied to the maze
        status_text : Status texts to display below the maze
        verbosity : Determines which visual effects are shown
        complete : Indicates the maze is complete, final image of the maze
        nostatus : Determines if the status text is shown below the maze
        redrawdelay : The minimum time between screen redraws

        Returns
        -------

        """
        if verbosity == 0:
            print(self.format_status(status_text), end="\r")
            if not complete:
                return

        maze_visual = self.add_visual_effects(visual_effects, verbosity)
        lines = ["".join(line) for line in maze_visual]
        time_since_last_show = time.time() - self.last_show_time
        if time_since_last_show < redrawdelay:
            time.sleep(redrawdelay - time_since_last_show)
        status_text["Time Elapsed"] = self.time_elapsed()
        output = "\n".join(lines)
        if not nostatus:
            output += f"\n{colorterm.RESET}{self.format_status(status_text)}"
        sys.stdout.write(ansitools.DEC_RESTORE_CURSOR_POSITION())
        sys.stdout.write(ansitools.DEC_SAVE_CURSOR_POSITION())
        sys.stdout.write(ansitools.MOVE_CURSOR_UP(len(self.visual_grid) + 2))
        sys.stdout.write(output)
        sys.stdout.flush()

        self.last_show_time = time.time()
