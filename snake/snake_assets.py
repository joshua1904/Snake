import pygame
from pathlib import Path

pygame.init()

SOURCE = Path("snake")

# Font
font = pygame.font.SysFont("comicsansms", 50)

# Sounds
eat_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/eat_sound.wav").resolve())
damage_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/damage.wav").resolve())
portal_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/portal.wav").resolve())
beat_highscore_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/beat_highscore.wav").resolve())
boost_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/boost.wav").resolve())

# Snake
snake_part = {
    'rl': pygame.image.load(Path(SOURCE, "images/textures/part_rl.bmp").resolve()),
    'ud': pygame.image.load(Path(SOURCE, "images/textures/part_ud.bmp").resolve()),
    'dr': pygame.image.load(Path(SOURCE, "images/textures/corner_dr.bmp").resolve()),
    'dl': pygame.image.load(Path(SOURCE, "images/textures/corner_dl.bmp").resolve()),
    'ur': pygame.image.load(Path(SOURCE, "images/textures/corner_ur.bmp").resolve()),
    'ul': pygame.image.load(Path(SOURCE, "images/textures/corner_ul.bmp").resolve())
}
snake_head = {
    'r': pygame.image.load(Path(SOURCE, "images/textures/head_l.bmp").resolve()),
    'u': pygame.image.load(Path(SOURCE, "images/textures/head_u.bmp").resolve()),
    'd': pygame.image.load(Path(SOURCE, "images/textures/head_d.bmp").resolve()),
    'l': pygame.image.load(Path(SOURCE, "images/textures/head_r.bmp").resolve())
}
snake_end = {
    'r': pygame.image.load(Path(SOURCE, "images/textures/end_r.bmp").resolve()),
    'u': pygame.image.load(Path(SOURCE, "images/textures/end_u.bmp").resolve()),
    'd': pygame.image.load(Path(SOURCE, "images/textures/end_d.bmp").resolve()),
    'l': pygame.image.load(Path(SOURCE, "images/textures/end_l.bmp").resolve())
}

# Map
wall_image = pygame.image.load(Path(SOURCE, "images/textures/wall.bmp").resolve())

portal_images = {
    1: pygame.image.load(Path(SOURCE, "images/textures/portal_1.bmp").resolve()),
    2: pygame.image.load(Path(SOURCE, "images/textures/portal_2.bmp").resolve()),
    3: pygame.image.load(Path(SOURCE, "images/textures/portal_3.bmp").resolve()),
}

sweet_image = pygame.image.load(Path(SOURCE, "images/textures/fruit.bmp").resolve())

# make black pixels transparent
for image in snake_part.values():
    image.set_colorkey("black")
for image in snake_head.values():
    image.set_colorkey("black")
for image in snake_end.values():
    image.set_colorkey("black")
for image in portal_images.values():
    image.set_colorkey("black")
sweet_image.set_colorkey("black")


