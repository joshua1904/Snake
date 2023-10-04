"""
Utils - import export
"""

import csv
import json
from pathlib import Path

SOURCE = Path("")
MAP_PATH = "maps/"
MAP_FILE_ENDING = ".csv"


def get_map(map_name):
    with open(Path(SOURCE, MAP_PATH + map_name + MAP_FILE_ENDING), "r") as f:
        return list(csv.reader(f, delimiter=";"))


def save_highscore(map_name, score):
    """
    Save highscore to json
    """
    highscore_json = get_json()
    highscore_json[map_name] = score
    print(highscore_json)
    with open(Path(SOURCE, "highscore.json").absolute(), "w") as f:
        json.dump(highscore_json, f)


def get_highscore(map_name):
    data = get_json()
    if map_name in data.keys():
        return data[map_name]
    return 0


def get_json():
    with open(Path(SOURCE, "highscore.json"), "r") as f:
        return json.load(f)


