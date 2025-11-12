import pathlib
from typing import Any, Type, Union

import tomli
from pydantic import BaseModel

tm_masks: dict[str, pathlib.Path] = dict()
masks_path = pathlib.Path(__file__).parent / "masks"
for mask in masks_path.iterdir():
    if mask.is_file() and mask.suffix == ".mask":
        tm_masks[mask.stem] = mask

tm_themes: dict[str, dict[str, dict[str, Any]]] = dict()
themes_path = pathlib.Path(__file__).parent / "themes"
for theme in themes_path.iterdir():
    if theme.is_file() and theme.suffix == ".toml":
        with theme.open(mode="rb") as theme_file:
            tm_themes[theme.stem] = tomli.load(theme_file)


class WallPathModel(BaseModel):
    character: str
    color: int | str


class RandomGroupModel(BaseModel):
    layer: int
    verbosity: list[int]
    character: str


class ModifyCellModel(BaseModel):
    layer: int
    verbosity: list[int]
    color: int | str
    character: str


class AnimationModel(BaseModel):
    layer: int
    cycles: list[int] | int
    animation_details: list[list[list[str | int] | str | int] | None]
    verbosity: list[int]


class AldousBroderTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    working_cell: AnimationModel
    last_linked: AnimationModel
    invalid_neighbors: AnimationModel
    invalid_visited: AnimationModel
    maximum_searching_frame_delay: float


class BinaryTreeTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    working_cell: AnimationModel
    last_linked: AnimationModel
    neighbors: AnimationModel


class EllersTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    group_to_random_color: RandomGroupModel


class HuntAndKillTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    working_cell: AnimationModel
    invalid_neighbors: AnimationModel
    last_linked: AnimationModel
    hunt_cells: AnimationModel
    hunting_frames_skip: int


class KruskalsRandomizedTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    group_random_color: RandomGroupModel


class PrimsSimpleTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    working_cell: AnimationModel
    edges: AnimationModel
    invalid_neighbors: AnimationModel
    last_linked: AnimationModel
    edge_frame_ratio: int


class PrimsWeightedTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    working_cell: AnimationModel
    pending_weighted_links: ModifyCellModel
    new_weighted_links: AnimationModel
    unlinked_neighbors: AnimationModel
    last_linked: AnimationModel


class RecursiveBacktrackerTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    working_cell: AnimationModel
    stack: ModifyCellModel
    invalid_neighbors: AnimationModel
    last_linked: AnimationModel
    stack_added_cells: AnimationModel
    stack_removed_cells: AnimationModel
    backtrack_skip_frames: int


class RecursiveDivisionTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    working_cell: AnimationModel
    division_cell_east: AnimationModel
    division_cell_west: AnimationModel
    division_cell_north: AnimationModel
    division_cell_south: AnimationModel
    generating_links_cells: AnimationModel
    passage_cell: AnimationModel


class SideWinderTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    run: ModifyCellModel
    working_cell: AnimationModel
    last_linked: AnimationModel


class WilsonsTheme(BaseModel):
    wall: WallPathModel
    path: WallPathModel
    target: ModifyCellModel
    working_cell: AnimationModel
    searching_walk: ModifyCellModel
    linking_walk: ModifyCellModel
    new_linked_walk: AnimationModel
    last_linked: AnimationModel
    searching_frames_skipped: int


class BreadthFirstTheme(BaseModel):
    working_cell: ModifyCellModel
    frontier: ModifyCellModel
    visited: ModifyCellModel
    visited_animation: AnimationModel
    target: ModifyCellModel
    solution_path: ModifyCellModel
    solution_animation: AnimationModel


class BreadthFirstEarlyExitTheme(BaseModel):
    working_cell: ModifyCellModel
    frontier: ModifyCellModel
    visited: ModifyCellModel
    visited_animation: AnimationModel
    target: ModifyCellModel
    solution_path: ModifyCellModel
    solution_animation: AnimationModel


class GreedyBestFirst(BaseModel):
    working_cell: ModifyCellModel
    frontier: ModifyCellModel
    visited: ModifyCellModel
    visited_animation: AnimationModel
    target: ModifyCellModel
    solution_path: ModifyCellModel
    solution_animation: AnimationModel


MAZE_THEME = (
    AldousBroderTheme
    | BinaryTreeTheme
    | EllersTheme
    | HuntAndKillTheme
    | KruskalsRandomizedTheme
    | PrimsSimpleTheme
    | PrimsWeightedTheme
    | RecursiveBacktrackerTheme
    | RecursiveDivisionTheme
    | SideWinderTheme
    | WilsonsTheme
)
SOLVE_THEME = BreadthFirstTheme | BreadthFirstEarlyExitTheme | GreedyBestFirst
THEME = Union[MAZE_THEME, SOLVE_THEME]

model_map: dict[str, Type[THEME]] = {
    "aldous_broder": AldousBroderTheme,
    "binary_tree": BinaryTreeTheme,
    "ellers": EllersTheme,
    "hunt_and_kill": HuntAndKillTheme,
    "kruskals_randomized": KruskalsRandomizedTheme,
    "prims_simple": PrimsSimpleTheme,
    "prims_weighted": PrimsWeightedTheme,
    "recursive_backtracker": RecursiveBacktrackerTheme,
    "recursive_division": RecursiveDivisionTheme,
    "side_winder": SideWinderTheme,
    "wilsons": WilsonsTheme,
    "breadth_first": BreadthFirstTheme,
    "breadth_first_early_exit": BreadthFirstEarlyExitTheme,
    "greedy_best_first": GreedyBestFirst,
}
themes: dict[str, dict[str, THEME]] = {theme_name: dict() for theme_name in tm_themes}
for theme_name, algorithms in tm_themes.items():
    for algorithm, theme_data in algorithms.items():
        themes[theme_name][algorithm] = model_map[algorithm].model_validate(theme_data)
