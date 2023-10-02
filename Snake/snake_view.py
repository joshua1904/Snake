"""
The front-end with pygame
"""
from pathlib import Path

import snake_classes
import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


SOURCE = Path("Snake")

eat_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/eat_sound.wav"))
damage_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/damage.wav"))
portal_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/portal.wav"))
click_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/click.wav"))
beat_highscore_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/beat_highscore.wav"))
boost_sound = pygame.mixer.Sound(Path(SOURCE, "sounds/boost.wav"))

# r right l left u up d down (snake move direction)
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


# make black pixels transparent
snake_part_rl.set_colorkey("black")
snake_part_ud.set_colorkey("black")
snake_corner_dr.set_colorkey("black")
snake_corner_dl.set_colorkey("black")
snake_corner_ur.set_colorkey("black")
snake_corner_ul.set_colorkey("black")
snake_head_r.set_colorkey("black")
snake_head_u.set_colorkey("black")
snake_head_d.set_colorkey("black")
snake_head_l.set_colorkey("black")
snake_end_r.set_colorkey("black")
snake_end_u.set_colorkey("black")
snake_end_d.set_colorkey("black")
snake_end_l.set_colorkey("black")
portal_image.set_colorkey("black")
sweet_image.set_colorkey("black")


def init_map_surface(board: snake_classes.GameBoard) -> pygame.Surface:
    map_surface = screen.copy()
    map_surface.fill("black")
    border = pygame.Surface((MAP_WIDTH * (SIZE + 2), MAP_HEIGHT * (SIZE + 2)))
    border.fill("darkorchid4")
    draw_picture(border, -1, -1, map_surface)
    background_surface = utils.create_background(wall_part, (MAP_WIDTH * SIZE, MAP_HEIGHT * SIZE))
    draw_picture(background_surface, 0, 0, map_surface)
    for wall in walls:
        draw_picture(wall_part, wall[0], wall[1], map_surface)
    draw_picture(portal_image, portal1[0], portal1[1], map_surface)
    draw_picture(portal_image, portal2[0], portal2[1], map_surface)


def create_background(image: pygame.image, map_size, tile_size=(360, 360), darker=90) -> pygame.Surface:
    """Generate Background-Imgae"""
    scaled_image = pygame.transform.smoothscale(image, tile_size)
    scaled_image.fill((darker, darker, darker), special_flags=pygame.BLEND_RGB_SUB)
    background_surface = pygame.Surface(map_size)
    for x in range(0, map_size[0] // tile_size[0] + 1):
        for y in range(0, map_size[1] // tile_size[1] + 1):
            background_surface.blit(scaled_image, (x * tile_size[0], y * tile_size[1]))
    return background_surface


def game_loop():

    while True:
        pygame.display.flip()
        clock.tick(10)  # limits FPS to 60


if __name__ == "__main__":
    game_loop()

