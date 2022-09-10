from terminalmaze.resources.cell import Cell
from dataclasses import dataclass
from typing import DefaultDict, Union


@dataclass
class Effect:
    """Apply a visual effect to the cell(s).

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
    """

    layer: int

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
        groups (Union[dict[int, list[Cell]], DefaultDict[int, list[Cell]]]): Group ID's mapped
        to lists of cells to be colored.
    """

    groups: Union[dict[int, list[Cell]], DefaultDict[int, list[Cell]]]


@dataclass
class TrailingColor(Effect):
    """Color cells with a trailing effect based on a list of colors provided such that cells[0] receives
    colors[0], cells[1] receives colors[1], etc. If cells and colors are different lenghts, the shortest
    list will be used.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn over lower layers.
        cells (list[Cell]): List of cells to be colored.
        colors (list[int]): List of colored.fg integers specifying the color. (0 -> 255)

    """

    cells: list[Cell]
    colors: list[int]


VisualEffect = Union[ColorSingleCell, ColorMultipleCells, RandomColorGroup, TrailingColor]
