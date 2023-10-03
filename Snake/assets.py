import pygame
from pathlib import Path

pygame.init()

SOURCE = Path("")

# Font
font = pygame.font.SysFont("comicsansms", 50)

# Sounds
eat_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/eat_sound.wav"))
damage_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/damage.wav"))
portal_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/portal.wav"))
click_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/click.wav"))
beat_highscore_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/beat_highscore.wav"))
boost_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/boost.wav"))

# Snake
snake_part = {
    'rl': pygame.image.load(Path(SOURCE, "pictures/textures/part_rl.bmp")),
    'ud': pygame.image.load(Path(SOURCE, "pictures/textures/part_ud.bmp")),
    'dr': pygame.image.load(Path(SOURCE, "pictures/textures/corner_dr.bmp")),
    'dl': pygame.image.load(Path(SOURCE, "pictures/textures/corner_dl.bmp")),
    'ur': pygame.image.load(Path(SOURCE, "pictures/textures/corner_ur.bmp")),
    'ul': pygame.image.load(Path(SOURCE, "pictures/textures/corner_ul.bmp"))
}
snake_head = {
    'r': pygame.image.load(Path(SOURCE, "pictures/textures/head_r.bmp")),
    'u': pygame.image.load(Path(SOURCE, "pictures/textures/head_u.bmp")),
    'd': pygame.image.load(Path(SOURCE, "pictures/textures/head_d.bmp")),
    'l': pygame.image.load(Path(SOURCE, "pictures/textures/head_l.bmp"))
}
snake_end = {
    'r': pygame.image.load(Path(SOURCE, "pictures/textures/end_r.bmp")),
    'u': pygame.image.load(Path(SOURCE, "pictures/textures/end_u.bmp")),
    'd': pygame.image.load(Path(SOURCE, "pictures/textures/end_d.bmp")),
    'l': pygame.image.load(Path(SOURCE, "pictures/textures/end_l.bmp"))
}

# Map
wall_image = pygame.image.load(Path(SOURCE, "pictures/textures/wall.bmp"))
portal_image = pygame.image.load(Path(SOURCE, "pictures/textures/portal.bmp"))
sweet_image = pygame.image.load(Path(SOURCE, "pictures/textures/fruit.bmp"))

# make black pixels transparent
for image in snake_part.values():
    image.set_colorkey("black")
for image in snake_head.values():
    image.set_colorkey("black")
for image in snake_end.values():
    image.set_colorkey("black")
portal_image.set_colorkey("black")
sweet_image.set_colorkey("black")


