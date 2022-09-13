import pathlib
import tomli

path = pathlib.Path(__file__).parent / "conf.toml"
with path.open(mode="rb") as conf_file:
    tm_config = tomli.load(conf_file)
