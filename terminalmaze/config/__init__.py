from typing import Any
import pathlib
import tomli

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
