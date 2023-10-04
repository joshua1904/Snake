import pygame
from pathlib import Path

pygame.init()

SOURCE = Path("")

# Font
font = pygame.font.SysFont("comicsansms", 50)

# Sounds
click_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/click.wav"))

# Mini-Map
wall_image = pygame.image.load(Path(SOURCE, "snake/images/textures/wall.bmp"))
portal_image = pygame.image.load(Path(SOURCE, "snake/images/textures/portal.bmp"))

