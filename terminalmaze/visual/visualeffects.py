from typing import DefaultDict
from types import SimpleNamespace

from terminalmaze.config import AnimationModel, ModifyCellModel, RandomGroupModel
from terminalmaze.resources.cell import Cell

GroupType = dict[int, list[Cell]] | DefaultDict[int, list[Cell]] | dict[int, set[Cell]] | DefaultDict[int, set[Cell]]


class Effect:
    """Apply a visual effect to the cell(s)."""

    def __init__(self, theme_data: ModifyCellModel | AnimationModel | RandomGroupModel):
        """
        Args:
            theme_data (LayerColor | AnimationModel): Colors and effects are drawn in layer order. Higher layers are
        drawn over lower layers.
            category (ve.Category): Category of the Effect to be applied at specific verbosity
        levels.
        """
        self.layer = theme_data.layer

    def __lt__(self, other: "Effect"):
        return self.layer < other.layer


class ModifySingleCell(Effect):
    """Color a single cell the given color."""

    def __init__(self, theme_data: ModifyCellModel):
        super().__init__(theme_data)
        self.cell: Cell = Cell(0, 0)
        self.color: int | str = theme_data.color
        self.character: str = theme_data.character
        self.verbosity: list[int] = theme_data.verbosity


class ModifyMultipleCells(Effect):
    """Color multiple cells the same color."""

    def __init__(self, theme_data: ModifyCellModel):
        super().__init__(theme_data)
        self.cells: list[Cell] = list()
        self.color: int | str = theme_data.color
        self.character: str = theme_data.character
        self.verbosity: list[int] = theme_data.verbosity


class RandomColorGroup(Effect):
    """Color groups of cells with randomly chosen colors. Colors will be
    assigned to groups and persist between show() calls."""

    def __init__(self, theme_data: RandomGroupModel):
        super().__init__(theme_data)
        self.groups: GroupType
        self.character: str = theme_data.character
        self.verbosity: list[int] = theme_data.verbosity


class Animation(Effect):
    def __init__(self, theme_data: AnimationModel):
        """Color cells with animating colors and characters."""
        super().__init__(theme_data)
        self.cells: list[Cell | None] = list()
        self.animating: dict[tuple[int, int], SimpleNamespace] = dict()
        self.cycles: list[int] | int = theme_data.cycles
        self.animation_details: list[list[list[str | int] | str | int] | None] = theme_data.animation_details
        self.animation_completed_passages: set[tuple[int, int]] = set()
        self.verbosity: list[int] = theme_data.verbosity

    def __lt__(self, other: "Effect"):
        return self.layer < other.layer


VisualEffect = ModifySingleCell | ModifyMultipleCells | RandomColorGroup | Animation
