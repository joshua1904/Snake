"""
Utils - import export
"""

import csv
import json
from pathlib import Path
from Snake.assets import SOURCE


def get_map(map_name):
    with open(Path(SOURCE, map_name), "r") as f:
        return list(csv.reader(f, delimiter=";"))


def set_highscore(map_str, score):
    """
    Save highscore to json
    """
    highscore_json = get_json()
    highscore_json[map_str] = score
    print(highscore_json)
    with open(Path(SOURCE, "highscore.json").absolute(), "w") as f:
        json.dump(highscore_json, f)


def get_highscore(map_str):
    data = get_json()
    if map_str in data.keys():
        return data[map_str]
    return 0


def get_json():
    with open(Path(SOURCE, "highscore.json"), "r") as f:
        return json.load(f)


