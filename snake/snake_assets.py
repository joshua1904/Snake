import pygame as pg
from pathlib import Path

from settings import SOURCE

pg.init()

# Font
# font = pg.font.SysFont("comicsansms", 50)
font = pg.font.Font(None, 64)

# Sounds
beat_highscore_sound = pg.mixer.Sound(Path(SOURCE, "snake",  "sounds/beat_highscore.wav").resolve())

# Sounds Snake 1
eat_sound = pg.mixer.Sound(Path(SOURCE, "snake", "sounds/eat_sound.wav").resolve())
damage_sound = pg.mixer.Sound(Path(SOURCE, "snake",  "sounds/damage.wav").resolve())
portal_sound = pg.mixer.Sound(Path(SOURCE, "snake",  "sounds/portal.wav").resolve())
boost_sound = pg.mixer.Sound(Path(SOURCE, "snake", "sounds/boost.wav").resolve())

# Sounds Snake 2
eat_sound_2 = pg.mixer.Sound(Path(SOURCE, "snake", "sounds/eat_sound_evil.wav").resolve())
damage_sound_2 = pg.mixer.Sound(Path(SOURCE, "snake",  "sounds/damage_evil.wav").resolve())
portal_sound_2 = pg.mixer.Sound(Path(SOURCE, "snake",  "sounds/portal_evil.wav").resolve())
boost_sound_2 = pg.mixer.Sound(Path(SOURCE, "snake", "sounds/boost_evil.wav").resolve())

# Snake
snake_part = {
    'rl': pg.image.load(Path(SOURCE, "snake", "images/textures/part_rl.bmp").resolve()),
    'ud': pg.image.load(Path(SOURCE, "snake", "images/textures/part_ud.bmp").resolve()),
    'dr': pg.image.load(Path(SOURCE, "snake", "images/textures/corner_dr.bmp").resolve()),
    'dl': pg.image.load(Path(SOURCE, "snake", "images/textures/corner_dl.bmp").resolve()),
    'ur': pg.image.load(Path(SOURCE, "snake", "images/textures/corner_ur.bmp").resolve()),
    'ul': pg.image.load(Path(SOURCE, "snake", "images/textures/corner_ul.bmp").resolve())
}
snake_head = {
    'r': pg.image.load(Path(SOURCE, "snake", "images/textures/head_l.bmp").resolve()),
    'u': pg.image.load(Path(SOURCE, "snake", "images/textures/head_u.bmp").resolve()),
    'd': pg.image.load(Path(SOURCE, "snake", "images/textures/head_d.bmp").resolve()),
    'l': pg.image.load(Path(SOURCE, "snake", "images/textures/head_r.bmp").resolve())
}
snake_end = {
    'r': pg.image.load(Path(SOURCE, "snake", "images/textures/end_r.bmp").resolve()),
    'u': pg.image.load(Path(SOURCE, "snake", "images/textures/end_u.bmp").resolve()),
    'd': pg.image.load(Path(SOURCE, "snake", "images/textures/end_d.bmp").resolve()),
    'l': pg.image.load(Path(SOURCE, "snake", "images/textures/end_l.bmp").resolve())
}

# Snake 2
snake_part_2 = {
    'rl': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/part_rl.bmp").resolve()),
    'ud': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/part_ud.bmp").resolve()),
    'dr': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/corner_dr.bmp").resolve()),
    'dl': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/corner_dl.bmp").resolve()),
    'ur': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/corner_ur.bmp").resolve()),
    'ul': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/corner_ul.bmp").resolve())
}
snake_head_2 = {
    'r': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/head_l.bmp").resolve()),
    'u': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/head_u.bmp").resolve()),
    'd': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/head_d.bmp").resolve()),
    'l': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/head_r.bmp").resolve())
}
snake_end_2 = {
    'r': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/end_r.bmp").resolve()),
    'u': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/end_u.bmp").resolve()),
    'd': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/end_d.bmp").resolve()),
    'l': pg.image.load(Path(SOURCE, "snake", "images/textures/evil/end_l.bmp").resolve())
}

# Map
wall_image = pg.image.load(Path(SOURCE, "snake", "images/textures/wall.bmp").resolve())

portal_images = {
    1: pg.image.load(Path(SOURCE, "snake", "images/textures/portal_1.bmp").resolve()),
    2: pg.image.load(Path(SOURCE, "snake", "images/textures/portal_2.bmp").resolve()),
    3: pg.image.load(Path(SOURCE, "snake", "images/textures/portal_3.bmp").resolve()),
}

sweet_image = pg.image.load(Path(SOURCE, "snake", "images/textures/fruit.bmp").resolve())

# make black pixels transparent
for image in snake_part.values():
    image.set_colorkey("black")
for image in snake_head.values():
    image.set_colorkey("black")
for image in snake_end.values():
    image.set_colorkey("black")
for image in snake_part_2.values():
    image.set_colorkey("black")
for image in snake_head_2.values():
    image.set_colorkey("black")
for image in snake_end_2.values():
    image.set_colorkey("black")
for image in portal_images.values():
    image.set_colorkey("black")
sweet_image.set_colorkey("black")


