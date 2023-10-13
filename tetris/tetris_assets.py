import pygame as pg
from pathlib import Path

from settings import SOURCE

pg.init()

game_sound = pg.mixer.Sound("/home/joshua/PycharmProjects/Snake2/tetris/sounds/sound.mp3")
clear_row = pg.mixer.Sound("/home/joshua/PycharmProjects/Snake2/tetris/sounds/clear_row.mp3")
highscore_json = Path("/home/joshua/PycharmProjects/Snake2/tetris/highscore.json")
font = pg.font.Font(None, 50)