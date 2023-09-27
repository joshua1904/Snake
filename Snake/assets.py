import pygame
from pathlib import Path

pygame.init()

clock = pygame.time.Clock()
SOURCE = Path("/home/joshua/PycharmProjects/GamingMachine/Snake")
FULLSCREEN = pygame.FULLSCREEN

#### SNAKE VARS ###########
eat_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/eat_sound.wav"))
damage_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/damage.wav"))
portal_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/portal.wav"))
click_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/click.wav"))
beat_highscore_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/beat_highscore.wav"))
boost_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/boost.wav"))
# r right l left u up d down (snake move direction
snake_part_rl = pygame.image.load(Path(SOURCE, "pictures/textures/part_rl.bmp"))
snake_part_ud = pygame.image.load(Path(SOURCE, "pictures/textures/part_ud.bmp"))

snake_corner_dr = pygame.image.load(Path(SOURCE, "pictures/textures/corner_dr.bmp"))
snake_corner_dl = pygame.image.load(Path(SOURCE, "pictures/textures/corner_dl.bmp"))
snake_corner_ur = pygame.image.load(Path(SOURCE, "pictures/textures/corner_ur.bmp"))
snake_corner_ul = pygame.image.load(Path(SOURCE, "pictures/textures/corner_ul.bmp"))

snake_head_r = pygame.image.load(Path(SOURCE, "pictures/textures/head_r.bmp"))
snake_head_u = pygame.image.load(Path(SOURCE, "pictures/textures/head_u.bmp"))
snake_head_d = pygame.image.load(Path(SOURCE, "pictures/textures/head_d.bmp"))
snake_head_l = pygame.image.load(Path(SOURCE, "pictures/textures/head_l.bmp"))

snake_end_r = pygame.image.load(Path(SOURCE, "pictures/textures/end_r.bmp"))
snake_end_u = pygame.image.load(Path(SOURCE, "pictures/textures/end_u.bmp"))
snake_end_d = pygame.image.load(Path(SOURCE, "pictures/textures/end_d.bmp"))
snake_end_l = pygame.image.load(Path(SOURCE, "pictures/textures/end_l.bmp"))

wall_part = pygame.image.load(Path(SOURCE, "pictures/textures/wall.bmp"))

portal_image = pygame.image.load(Path(SOURCE, "pictures/textures/portal.bmp"))

sweet_image = pygame.image.load(Path(SOURCE, "pictures/textures/fruit.bmp"))

font = pygame.font.SysFont("comicsansms", 50)