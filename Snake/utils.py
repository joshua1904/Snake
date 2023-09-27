import csv
import random
import json
from pathlib import Path
from Snake.assets import SOURCE
import pygame


def get_map(map_name):
    with open(Path(SOURCE, map_name), "r") as f:
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


def create_background(image: pygame.image, map_size, tile_size=(360, 360), darker=90) -> pygame.Surface:
    """Generate Background-Imgae"""
    scaled_image = pygame.transform.smoothscale(image, tile_size)
    scaled_image.fill((darker, darker, darker), special_flags=pygame.BLEND_RGB_SUB)
    background_surface = pygame.Surface(map_size)
    for x in range(0, map_size[0] // tile_size[0] + 1):
        for y in range(0, map_size[1] // tile_size[1] + 1):
            background_surface.blit(scaled_image, (x * tile_size[0], y * tile_size[1]))
    return background_surface



def create_map_from_image(image: pygame.Surface):
    """Image has to be a black and white bitmap, white pixels are walls, size of image is size of map"""
    for y in range(0, image.get_height()):
        for x in range(0, image.get_width()):
            color = image.get_at((x, y))
            if color.r >= 250:
                print("1;", end="")
            elif color.r <= 10:
                print("0;", end="")
        print("")

