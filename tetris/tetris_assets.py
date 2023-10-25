import pygame as pg
from pathlib import Path

from settings import SOURCE

pg.init()

game_sound = pg.mixer.Sound("/home/joshua/PycharmProjects/Snake2/tetris/sounds/sound.mp3")
clear_row = pg.mixer.Sound("/home/joshua/PycharmProjects/Snake2/tetris/sounds/clear_row.mp3")
highscore_json = Path("/home/joshua/PycharmProjects/Snake2/tetris/highscore.json")
img_normal = pg.image.load("/home/joshua/PycharmProjects/Snake2/snake/images/textures/head_d.bmp")
img_right = pg.transform.rotate(img_normal, 90)
img_down = pg.transform.rotate(img_normal, 180)
img_left = pg.transform.rotate(img_normal, 270)
font = pg.font.Font(None, 50)