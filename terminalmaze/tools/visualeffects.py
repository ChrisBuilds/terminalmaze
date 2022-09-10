from terminalmaze.resources.cell import Cell
from dataclasses import dataclass
from typing import DefaultDict, Union


@dataclass
class Effect:
    """Apply a visual effect to the cell(s).

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn
        over lower layers.
    """

    layer: int

    def __lt__(self, other: "Effect"):
        return self.layer < other.layer


@dataclass
class Single(Effect):
    """Color a single cell the given color.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn
        over lower layers.
        cell (Cell): Cell to be colored.
        color (int): colored.fg integer specifying the color. (0 -> 255)
    """

    cell: Cell
    color: int


@dataclass
class Multiple(Effect):
    """Color multiple cells the same color.

    Args:
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn
        over lower layers.
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
        layer (int): Colors and effects are drawn in layer order. Higher layers are drawn
        over lower layers.
        groups (Union[dict[int, list[Cell]], DefaultDict[int, list[Cell]]]): Group ID's mapped
        to lists of cells to be colored.
    """

    groups: Union[dict[int, list[Cell]], DefaultDict[int, list[Cell]]]


VisualEffect = Union[Single, Multiple, RandomColorGroup]
