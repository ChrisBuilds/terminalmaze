from terminalmaze.resources.cell import Cell
from dataclasses import dataclass
from typing import DefaultDict, Literal
import random


GroupType = dict[int, list[Cell]] | DefaultDict[int, list[Cell]] | dict[int, set[Cell]] | DefaultDict[int, set[Cell]]
LOGIC: Literal["logic"] = "logic"
STYLE: Literal["style"] = "style"
LOGICSTYLE: Literal["logicstyle"] = "logicstyle"
Category = Literal["logic", "style", "logicstyle"]
Theme = dict[str, dict[str, int | list[int]]]


@dataclass
class Effect:
    """Apply a visual effect to the cell(s).

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
        category (ve.Category): Category of the Effect to be applied at specific verbosity levels.
    """

    layer: int
    category: Category

    def __lt__(self, other: "Effect"):
        return self.layer < other.layer


@dataclass
class ColorSingleCell(Effect):
    """Color a single cell the given color.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
        cell (Cell): Cell to be colored.
        color (int): colored.fg integer specifying the color. (0 -> 255)
    """

    cell: Cell
    color: int


@dataclass
class ColorMultipleCells(Effect):
    """Color multiple cells the same color.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
        cells (list[Cell]): List of cells to be colored.
        color (int): colored.fg integer specifying the color. (0 -> 255)
    """

    cells: list[Cell]
    color: int


@dataclass
class RandomColorGroup(Effect):
    """Color groups of cells with randomly chosen colors. Colors will be
    assigned to groups and persist between show() calls.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
        groups (GroupType): Group ID's mapped
        to lists of cells to be colored.
    """

    groups: GroupType


@dataclass
class ColorTrail(Effect):
    """Color cells with a trailing effect based on a list of colors provided such that cells[0] receives
    colors[0], cells[1] receives colors[1], etc. If cells and colors are different lenghts, the shortest
    list will be used.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
        cells (list[Cell]): List of cells to be colored.
        colors (list[int]): List of colored.fg integers specifying the color. (0 -> 255)
        traveldir (int): Direction the colors will rotate across the trail: -1 = forward, 0 = None, 1 = backward

    """

    cells: list[Cell]
    colors: list[int]
    traveldir: int


@dataclass
class ColorTransition(Effect):
    """Color cells with a transitioning color with a transition speed based on frames per color.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
        cells (list[Cell]): List of cells to be colored.
        transitioning dict[tuple[int, int], list[int]]: Used by the visualizing function to handle cells
        colors (list[int]): List of colored.fg integers specifying the color. (0 -> 255), 0 index is the first
                            color used for the transition
        frames_per_state (int): The number of frames to show each color prior to transitioning
    """

    cells: list[Cell]
    transitioning: dict[tuple[int, int], list[int]]
    colors: list[int]
    frames_per_state: int = 1


@dataclass
class CharacterTransition(Effect):
    cells: list[Cell]
    transitioning: dict[tuple[int, int], list[int]]
    characters: list[int]
    frames_per_state: int = 1


def random_binary_chars(length: int) -> list[str]:
    """
    Returns a list of 1 and 0 strings, of the given length.
    Parameters
    ----------
    length : int The number of strings to generate

    Returns
    -------
    List[str]
    """
    return [random.choice(("0", "1")) for _ in range(length)]


VisualEffect = ColorSingleCell | ColorMultipleCells | RandomColorGroup | ColorTrail | ColorTransition
