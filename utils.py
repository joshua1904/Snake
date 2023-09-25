import csv
import random
import json
def get_map(map_name):
    with open(map_name, "r") as f:
        return list(csv.reader(f, delimiter=";"))

def spawn_portal(MAP: list) -> tuple:
    for row_counter, row in enumerate(MAP):
        if "2" in row:
           portal1 = (row.index("2"), row_counter)
        if "3" in row:
            portal2 = (row.index("3"), row_counter)
    return portal1, portal2


def spawn_walls(walls: list, MAP: list):
    for row_counter, row in enumerate(MAP):
        for field_counter, field in enumerate(row):
            if field == "1":
                walls.append((field_counter, row_counter))

def spawn_sweet(SIZE, snake, walls, portals):
    sweet_x = random.randint(1, 1910 // SIZE)
    sweet_y = random.randint(1, 1070 // SIZE)
    if (sweet_xy := (sweet_x, sweet_y)) not in snake and sweet_xy not in walls and sweet_xy not in (portals[0], portals[1]):
        return sweet_xy
    else:
        return spawn_sweet(SIZE, snake, walls, portals)

def set_highscore(map_str, score):
    highscore_json = get_json()
    highscore_json[map_str] = score
    print(highscore_json)
    with open("highscore.json", "w") as f:
        json.dump(highscore_json, f)
def get_highscore(map_str):
    data = get_json()
    if map_str in data.keys():
        return data[map_str]
    return 0
def get_json():
    with open("highscore.json", "r") as f:
        return json.load(f)
set_highscore("test", 1)
#print(get_highscore("map1.csv"))
