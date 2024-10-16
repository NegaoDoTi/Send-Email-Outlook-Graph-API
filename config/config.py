from pathlib import Path
from json import load

with open(Path(Path(__file__).parent.parent, "config.json"), "r") as file: config_env = load(file)

