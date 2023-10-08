import pygame as pg
from pathlib import Path

from settings import SOURCE

pg.init()


# Font
font = pg.font.Font(None, 64)
font_small = pg.font.Font(None, 32)

# Sounds
click_sound = pg.mixer.Sound(Path(SOURCE, "sounds/click.wav").resolve())
victory_good_sound = pg.mixer.Sound(Path(SOURCE, "sounds/victory_good.wav").resolve())
victory_evil_sound = pg.mixer.Sound(Path(SOURCE, "sounds/victory_good.wav").resolve())
bravo_sound = pg.mixer.Sound(Path(SOURCE, "sounds/bravo.wav").resolve())

# Mini-Map
wall_image = pg.image.load(Path(SOURCE, "snake/images/textures/wall.bmp").resolve())
portal_images = {
    1: pg.image.load(Path(SOURCE, "snake/images/textures/portal_1.bmp").resolve()),
    2: pg.image.load(Path(SOURCE, "snake/images/textures/portal_2.bmp").resolve()),
    3: pg.image.load(Path(SOURCE, "snake/images/textures/portal_3.bmp").resolve()),
}

