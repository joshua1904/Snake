"""
Utils - import export
"""

import csv
import json
from typing import List

import pygame as pg
import menu_assets as ma
from pathlib import Path

from settings import SOURCE

MAP_PATH = "maps/"
MAP_FILE_ENDING = ".csv"


def get_map(map_name):
    with open(Path(SOURCE, MAP_PATH + map_name + MAP_FILE_ENDING).resolve(), "r") as f:
        map_list = list(csv.reader(f, delimiter=";"))
        return [row for row in map_list if row]         # remove empty rows (lines)


def get_all_map_names() -> List[str]:
    map_dir = Path(SOURCE, MAP_PATH)
    map_names = []
    for map_file in map_dir.glob("*.csv"):
        map_names.append(map_file.stem)
    return map_names


def save_highscore(map_name, score, name, message):
    """
    Save highscore to json
    """
    highscore_json = get_json()
    highscore_json[map_name] = {
        "score": score,
        "name": name,
        "message": message
    }
    # print(highscore_json)
    with open(Path(SOURCE, "highscore.json").resolve(), "w") as f:
        json.dump(highscore_json, f)


def get_highscore(map_name):
    data = get_json()
    if map_name in data.keys():
        return data[map_name]
    return {"score": 0, "name": "Noob", "message": "Ich bin ein Noob."}


def get_json():
    with open(Path(SOURCE, "highscore.json").resolve(), "r") as f:
        return json.load(f)


class InputBox:
    COLOR_INACTIVE = pg.Color('lightskyblue3')
    COLOR_ACTIVE = pg.Color('dodgerblue2')

    def __init__(self, x, y, w, h, text='', active=False, max_len=100):
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.active = active
        self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        self.txt_surface = ma.font_small.render(text, True, self.color)
        self.max_len = max_len
        self.bg_color = pg.Color(30, 30, 30)

    def handle_event(self, event):
        # if event.type == pg.MOUSEBUTTONDOWN:
        #     # If the user clicked on the input_box rect.
        #     if self.rect.collidepoint(event.pos):
        #         # Toggle the active variable.
        #         self.active = not self.active
        #     else:
        #         self.active = False
        #     # Change the current color of the input box.

        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_UP, pg.K_DOWN, pg.K_RETURN):
                self.active = not self.active
                self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE

            if self.active:
                # if event.key == pg.K_RETURN:
                #     print(self.text)
                #     self.text = ''
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    char = event.unicode
                    if ((char.isascii() and char.isalnum()) or char in ' !?.,-()<>') and len(self.text) <= self.max_len:
                        self.text += char

            # Re-render the text.
            self.txt_surface = ma.font_small.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        pg.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def create_map_from_image(image: pg.Surface):
    """Image has to be a black and white bitmap, white pixels are walls, size of image is size of map"""
    for y in range(0, image.get_height()):
        for x in range(0, image.get_width()):
            color = image.get_at((x, y))
            if color.r >= 250:
                print("1;", end="")
            elif color.r <= 10:
                print("0;", end="")
        print("")

i = pg.image.load(Path(SOURCE, "brainfuck.png"))
create_map_from_image(i)