import pygame
from pathlib import Path

from settings import SOURCE

pygame.init()


# Font
font = pygame.font.SysFont("comicsansms", 50)

# Sounds
click_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/click.wav").resolve())

# Mini-Map
wall_image = pygame.image.load(Path(SOURCE, "snake/images/textures/wall.bmp").resolve())
portal_images = {
    1: pygame.image.load(Path(SOURCE, "snake/images/textures/portal_1.bmp").resolve()),
    2: pygame.image.load(Path(SOURCE, "snake/images/textures/portal_2.bmp").resolve()),
    3: pygame.image.load(Path(SOURCE, "snake/images/textures/portal_3.bmp").resolve()),
}

