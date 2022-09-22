from typing import Any, Type
import pathlib
import tomli
from pydantic import BaseModel

tm_config: dict[str, dict[str, Any]]
path = pathlib.Path(__file__).parent / "conf.toml"
with path.open(mode="rb") as conf_file:
    tm_config = tomli.load(conf_file)

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


class LayerColor(BaseModel):
    layer: int
    color: int


class Transition(BaseModel):
    layer: int
    frames_per_value: int
    characters: list[str]
    colors: list[int]


class AldousBroderTheme(BaseModel):
    wall: int
    path: int
    working_cell: LayerColor
    last_linked: Transition
    invalid_neighbors: LayerColor
    invalid_visited: Transition


class BinaryTreeTheme(BaseModel):
    wall: int
    path: int
    working_cell: LayerColor
    neighbor: LayerColor


class EllersTheme(BaseModel):
    wall: int
    path: int
    group_to_random_color_layer: int


class KruskalsRandomizedTheme(BaseModel):
    wall: int
    path: int
    group_random_color_layer: int


class HuntAndKillTheme(BaseModel):
    wall: int
    path: int
    working_cell: LayerColor
    last_linked: LayerColor
    invalid_neighbors: LayerColor
    link_transition: Transition
    hunt_transition: Transition


class PrimsSimpleTheme(BaseModel):
    wall: int
    path: int
    working_cell: LayerColor
    edges: LayerColor
    invalid_neighbors: LayerColor
    last_linked: LayerColor
    old_edges: LayerColor


class PrimsWeightedTheme(BaseModel):
    wall: int
    path: int
    working_cell: LayerColor
    links: LayerColor
    unlinked_neighbors: LayerColor
    last_linked_transition: Transition


class RecursiveBacktrackerTheme(BaseModel):
    wall: int
    path: int
    working_cell: LayerColor
    stack: LayerColor
    invalid_neighbors: LayerColor
    last_linked: LayerColor
    stack_transition: Transition
    backtrack_transition: Transition


class SideWinderTheme(BaseModel):
    wall: int
    path: int
    run: LayerColor
    working_cell: LayerColor
    last_linked: LayerColor


class WilsonsTheme(BaseModel):
    wall: int
    path: int
    target: LayerColor
    walk: LayerColor
    working_cell: LayerColor
    link_transition: Transition


class BreadthFirstTheme(BaseModel):
    working_cell: LayerColor
    frontier: LayerColor
    visited: LayerColor
    visited_transition: Transition
    target: LayerColor
    solution_path: LayerColor
    solution_transition: Transition


THEME = (
    AldousBroderTheme
    | BinaryTreeTheme
    | EllersTheme
    | HuntAndKillTheme
    | KruskalsRandomizedTheme
    | PrimsSimpleTheme
    | PrimsWeightedTheme
    | RecursiveBacktrackerTheme
    | SideWinderTheme
    | WilsonsTheme
    | BreadthFirstTheme
)

model_map: dict[str, Type[THEME]] = {
    "aldous_broder": AldousBroderTheme,
    "binary_tree": BinaryTreeTheme,
    "ellers": EllersTheme,
    "hunt_and_kill": HuntAndKillTheme,
    "kruskals_randomized": KruskalsRandomizedTheme,
    "prims_simple": PrimsSimpleTheme,
    "prims_weighted": PrimsWeightedTheme,
    "recursive_backtracker": RecursiveBacktrackerTheme,
    "side_winder": SideWinderTheme,
    "wilsons": WilsonsTheme,
    "breadth_first": BreadthFirstTheme,
}
themes: dict[str, dict[str, THEME]] = {theme_name: dict() for theme_name in tm_themes}
for theme_name, algorithms in tm_themes.items():
    for algorithm, theme_data in algorithms.items():
        themes[theme_name][algorithm] = model_map[algorithm].parse_obj(theme_data)
