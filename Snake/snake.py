# Example file showing a basic pygame "game loop"
import collections

import pygame

from Snake import utils
from Snake.assets import *

# pygame setup


running = True
SIZE = 30
snake = list()
#saves direction changes of the snake
corner_save = dict()
speed = False
CURRENT_DIRECTION = "r"
wanted_direction = "r"
alive = True
score = 0
walls = list()

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

MAP = list()
MAP_WIDTH = 0
MAP_HEIGHT = 0
map_surface = pygame.Surface((1, 1))
portal1 = tuple()
portal2 = tuple()
sweet = tuple()

def init(map_str, screen):
    global portal1, portal2, sweet, snake, CURRENT_DIRECTION, wanted_direction, alive, running,\
        MAP, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, corner_save
    walls.clear()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    MAP = utils.get_map(map_str)
    MAP_WIDTH = len(MAP[0])
    MAP_HEIGHT = len(MAP) - 1
    utils.spawn_walls(walls, MAP)
    portal1, portal2 = utils.spawn_portal(MAP)
    utils.spawn_walls(walls, MAP)
    init_map_surface(screen)
    CURRENT_DIRECTION = "r"
    wanted_direction = "r"
    snake = [(10, 1), (11, 1)]
    corner_save = {(10, 1): "r", (11, 1): "r"}
    sweet = utils.spawn_sweet(MAP_WIDTH, MAP_HEIGHT, snake, walls, (portal1, portal2))
    alive = True
    running = True

def init_map_surface(screen):
    global map_surface
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

def draw_score(points: int, highscore: int, screen):
    text = font.render(f"{points} HIGSCORE: {highscore}", True, "blue")
    screen.blit(text,
                (SIZE + 10, SIZE + 10))

def reset():
    global snake
    global score
    global wanted_direction
    global CURRENT_DIRECTION
    wanted_direction = "r"
    CURRENT_DIRECTION = "r"
    score = 0
    snake = [(10, 0), (11, 0)]
    return True


def move(direction: str):
    match direction:
        case "r":
            move_right()
        case "u":
            move_up()
        case "d":
            move_down()
        case "l":
            move_left()
    if snake.count(snake[-1]) > 1 or walls.count(snake[-1]) > 1:
        return False
    return True

def draw_sweet(screen):
    draw_picture(sweet_image, sweet[0], sweet[1], screen)

def save_corner(pos, dir_before_move: str):
    global CURRENT_DIRECTION
    if dir_before_move != CURRENT_DIRECTION:
        corner_save[pos] = f"{dir_before_move}{CURRENT_DIRECTION}"
    else:
        corner_save[pos] = CURRENT_DIRECTION
def move_right():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "l":
        move_left()
        return
    CURRENT_DIRECTION = "r"
    head = snake[-1]
    snake.pop(0)

    if head == portal1:
        play_sound(portal_sound)
        snake.append((portal2[0] + 1, portal2[1]))
        save_corner((portal2[0], portal2[1]), dir_before_move)
        return
    if head == portal2:
        play_sound(portal_sound)
        snake.append((portal1[0] + 1, portal1[1]))
        save_corner((portal1[0], portal1[1]), dir_before_move)
        return
    if (head_x := head[0]) < MAP_WIDTH - 1:
        snake.append((head_x + 1, head[1]))
        save_corner((head_x, head[1]), dir_before_move)
    else:
        snake.append((0, head[1]))
        save_corner((head_x, head[1]), dir_before_move)
        save_corner((-1, head[1]), dir_before_move)


def move_left():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "r":
        move_right()
        return
    CURRENT_DIRECTION = "l"
    head = snake[-1]
    snake.pop(0)

    if head == portal1:
        play_sound(portal_sound)
        snake.append((portal2[0] - 1, portal2[1]))
        save_corner((portal2[0], portal2[1]), dir_before_move)
        return
    if head == portal2:
        play_sound(portal_sound)
        snake.append((portal1[0] - 1, portal1[1]))
        save_corner((portal1[0], portal1[1]), dir_before_move)
        return
    if (head_x := head[0]) > 0:
        snake.append((head_x - 1, head[1]))
        save_corner((head_x, head[1]), dir_before_move)
    else:
        snake.append((MAP_WIDTH - 1, head[1]))
        save_corner((head_x, head[1]), dir_before_move)
        save_corner((MAP_WIDTH, head[1]), dir_before_move)

def move_down():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "u":
        move_up()
        return
    CURRENT_DIRECTION = "d"
    head = snake[-1]
    snake.pop(0)

    if head == portal1:
        play_sound(portal_sound)
        snake.append((portal2[0], portal2[1] + 1))
        save_corner((portal2[0], portal2[1]), dir_before_move)
        return
    if head == portal2:
        play_sound(portal_sound)
        snake.append((portal1[0], portal1[1] + 1))
        save_corner((portal1[0], portal1[1]), dir_before_move)
        return
    if (head_y := head[1]) < MAP_HEIGHT - 1:
        snake.append((head[0], head_y + 1))
        save_corner((head[0], head_y), dir_before_move)
    else:
        snake.append((head[0], 0))
        save_corner((head[0], head_y), dir_before_move)
        save_corner((head[0], -1), dir_before_move)


def move_up():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "d":
        move_down()
        return
    CURRENT_DIRECTION = "u"
    head = snake[-1]
    snake.pop(0)

    if head == portal1:
        play_sound(portal_sound)
        snake.append((portal2[0], portal2[1] -1))
        save_corner((portal2[0], portal2[1]), dir_before_move)
        return
    if head == portal2:
        play_sound(portal_sound)
        snake.append((portal1[0], portal1[1] - 1))
        save_corner((portal1[0], portal1[1]), dir_before_move)
        return
    if (head_y := head[1]) > 0:
        snake.append((head[0], head_y - 1))
        save_corner((head[0], head_y), dir_before_move)
    else:
        snake.append((head[0], MAP_HEIGHT - 1))
        save_corner((head[0], head_y), dir_before_move)
        save_corner((head[0], MAP_HEIGHT), dir_before_move)
def add_body_part():
    global CURRENT_DIRECTION
    snake.append(sweet)


def check_sweet() -> bool:
    return snake[-1] == sweet

def draw_picture(image, x, y, surface):
    surface.blit(image, (x * SIZE + SCREEN_WIDTH // 2 - MAP_WIDTH * SIZE // 2,
                         y * SIZE + SCREEN_HEIGHT // 2 - MAP_HEIGHT * SIZE // 2))

def draw_snake_head(screen):
    head_x, head_y = snake[-1]
    if (head_x, head_y) not in (portal1, portal2):
        match CURRENT_DIRECTION:
            case "r":
                draw_picture(snake_head_l, head_x, head_y, screen)
            case "d":
                draw_picture(snake_head_d, head_x, head_y, screen)
            case "l":
                draw_picture(snake_head_r, head_x, head_y, screen)
            case "u":
                draw_picture(snake_head_u, head_x, head_y, screen)


def draw_snake_tail_part(x, y, screen):
    if (position := (x, y)) not in corner_save:
        return
    rotation = corner_save[position]
    last_snake_piece = position == snake[0]

    if last_snake_piece:
        #SORRY :( ber der code spart ein paat if abfragen weil man jetzt nur aufs ende von der rotation schauen muss
        match rotation[-1]:
            case "r":             # rotation in ("r" "ur" "dr")
                draw_picture(snake_end_r, x, y, screen)
            case "l":
                draw_picture(snake_end_l, x, y, screen)
            case "u":
                draw_picture(snake_end_u, x, y, screen)
            case "d":
                draw_picture(snake_end_d, x, y, screen)
    else:
        match rotation:
            case "r" | "l":
                draw_picture(snake_part_rl, x, y, screen)
            case "u" | "d":
                draw_picture(snake_part_ud, x, y, screen)
            case "rd" | "ul":
                draw_picture(snake_corner_dr, x, y, screen)
            case "dr" | "lu":
                draw_picture(snake_corner_ul, x, y, screen)
            case "ru" | "dl":
                draw_picture(snake_corner_ur, x, y, screen)
            case "ur" | "ld":
                draw_picture(snake_corner_dl, x, y, screen)

    keys_to_delete = [key for key in corner_save.keys() if key not in snake]
    for i in keys_to_delete:
        corner_save.pop(i)

def draw_snake_tail(screen):
    for part in snake:
        draw_snake_tail_part(part[0], part[1], screen)

def draw_snake(screen):
    draw_snake_head(screen)
    draw_snake_tail(screen)

def draw_map(screen):
    screen.blit(map_surface, (0, 0))

def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()
def game_loop(map_str, screen):

    highscore_set = False
    global running
    global alive
    global wanted_direction
    score = 0
    global sweet
    global speed
    init(map_str, screen)
    highscore = utils.get_highscore(map_str)
    current_highscore = highscore
    speed_count = 0
    speed = False
    last_direction = CURRENT_DIRECTION

    # nur bestimmte events speichern (Mausbewegung zb ausschließen)
    pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP))
    pressed_direction_keys_queue = collections.deque(list())

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_HASH:
                            alive = reset()
                        case pygame.K_SPACE:
                            speed = True
                        case pygame.K_LEFT:
                            pressed_direction_keys_queue.append("l")
                        case pygame.K_RIGHT:
                            pressed_direction_keys_queue.append("r")
                        case pygame.K_UP:
                            pressed_direction_keys_queue.append("u")
                        case pygame.K_DOWN:
                            pressed_direction_keys_queue.append("d")
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_SPACE:
                            speed = False

        if not pressed_direction_keys_queue:
            alive = move(CURRENT_DIRECTION)
            last_direction = CURRENT_DIRECTION
        else:
            while pressed_direction_keys_queue:         # filter consecutive same directions like 'r', 'r', 'r'
                wanted_direction = pressed_direction_keys_queue.popleft()
                if wanted_direction != last_direction:
                    last_direction = wanted_direction
                    break
            alive = move(wanted_direction)

        if alive:
            # fill the screen with a color to wipe away anything from last frame
            draw_map(screen)
            draw_sweet(screen)
            draw_snake(screen)

            if check_sweet():
                play_sound(eat_sound)
                score += 1
                add_body_part()
                sweet = utils.spawn_sweet(MAP_WIDTH, MAP_HEIGHT, snake, walls, (portal1, portal2))
                if score > highscore:
                    highscore = score
                    if not highscore_set:
                        play_sound(beat_highscore_sound)
                        highscore_set = True

            draw_score(score, highscore, screen)
            # flip() the display to put your work on screen
            pygame.display.flip()
        else:
            play_sound(damage_sound)
            if highscore > current_highscore:
                utils.set_highscore(map_str, highscore)
            return
        if speed:
            if speed_count % 10 == 0:
                play_sound(boost_sound)
            clock.tick(20)
            speed_count += 1
        else:
            clock.tick(4)  # limits FPS to 60
            speed_count = 0
