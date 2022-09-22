from terminalmaze.resources.cell import Cell
from typing import DefaultDict
from terminalmaze.config import LayerColor, Transition, LayerVerbosity


GroupType = dict[int, list[Cell]] | DefaultDict[int, list[Cell]] | dict[int, set[Cell]] | DefaultDict[int, set[Cell]]


class Effect:
    """Apply a visual effect to the cell(s)."""

    def __init__(self, theme_data: LayerColor | Transition | LayerVerbosity):
        """
        Args:
            theme_data (LayerColor | Transition): Colors and effects are drawn in layer order. Higher layers are
        drawn over lower layers.
            category (ve.Category): Category of the Effect to be applied at specific verbosity
        levels.
        """
        self.layer = theme_data.layer

    def __lt__(self, other: "Effect"):
        return self.layer < other.layer


class ColorSingleCell(Effect):
    """Color a single cell the given color."""

    def __init__(self, theme_data: LayerColor):
        super().__init__(theme_data)
        self.cell: Cell = Cell(0, 0)
        self.color: int = theme_data.color
        self.character: str = theme_data.character
        self.verbosity: list[int] = theme_data.verbosity


class ColorMultipleCells(Effect):
    """Color multiple cells the same color."""

    def __init__(self, theme_data: LayerColor):
        super().__init__(theme_data)
        self.cells: list[Cell] = list()
        self.color: int = theme_data.color
        self.character: str = theme_data.character
        self.verbosity: list[int] = theme_data.verbosity


class RandomColorGroup(Effect):
    """Color groups of cells with randomly chosen colors. Colors will be
    assigned to groups and persist between show() calls."""

    def __init__(self, theme_data: LayerVerbosity):
        super().__init__(theme_data)
        self.groups: GroupType
        self.character: str = theme_data.character
        self.verbosity: list[int] = theme_data.verbosity


class ValueTransition(Effect):
    def __init__(self, theme_data: Transition):
        """Color cells with a transitioning colors and characters with a transition speed based on frames per color."""
        super().__init__(theme_data)
        self.cells: list[Cell] = list()
        self.transitioning: dict[tuple[int, int], list[int]] = dict()
        self.colors: list[int] = theme_data.colors
        self.characters: list[str] = theme_data.characters
        self.frames_per_value: int = theme_data.frames_per_value
        self.verbosity: list[int] = theme_data.verbosity

    def __lt__(self, other: "Effect"):
        return self.layer < other.layer


VisualEffect = ColorSingleCell | ColorMultipleCells | RandomColorGroup | ValueTransition
