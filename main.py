# Example file showing a basic pygame "game loop"
import collections

import pygame
import utils

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
SIZE = 30
snake = list()
#safes direction changes of the snake
corner_safe = dict()
speed = False
CURRENT_DIRECTION = "r"
wanted_direction = "r"
alive = True
score = 0
font = pygame.font.SysFont("comicsansms", 72)
walls = list()

eat_sound = pygame.mixer.Sound("sounds/eat_sound.wav")
damage_sound = pygame.mixer.Sound("sounds/damage.wav")
portal_sound = pygame.mixer.Sound("sounds/portal.wav")
click_sound = pygame.mixer.Sound("sounds/click.wav")
beat_highscore_sound = pygame.mixer.Sound("sounds/beat_highscore.wav")
boost_sound = pygame.mixer.Sound("sounds/boost.wav")
# r right l left u up d down (snake move direction
snake_part_rl = pygame.image.load("pictures/textures/part_rl.bmp")
snake_part_ud = pygame.image.load("pictures/textures/part_ud.bmp")

snake_corner_dr = pygame.image.load("pictures/textures/corner_dr.bmp")
snake_corner_dl = pygame.image.load("pictures/textures/corner_dl.bmp")
snake_corner_ur = pygame.image.load("pictures/textures/corner_ur.bmp")
snake_corner_ul = pygame.image.load("pictures/textures/corner_ul.bmp")

snake_head_r = pygame.image.load("pictures/textures/head_r.bmp")
snake_head_u = pygame.image.load("pictures/textures/head_u.bmp")
snake_head_d = pygame.image.load("pictures/textures/head_d.bmp")
snake_head_l = pygame.image.load("pictures/textures/head_l.bmp")

snake_end_r = pygame.image.load("pictures/textures/end_r.bmp")
snake_end_u = pygame.image.load("pictures/textures/end_u.bmp")
snake_end_d = pygame.image.load("pictures/textures/end_d.bmp")
snake_end_l = pygame.image.load("pictures/textures/end_l.bmp")

wall_part = pygame.image.load("pictures/textures/wall.bmp")


portal_image = pygame.image.load("pictures/textures/portal.bmp")

sweet_image = pygame.image.load("pictures/textures/fruit.bmp")
MAP = list()
portal1 = tuple()
portal2 = tuple()
sweet = tuple()

def init(map_str):
    global portal1, portal2, sweet, snake, CURRENT_DIRECTION, wanted_direction, alive, running, MAP, corner_safe
    walls.clear()
    MAP = utils.get_map(map_str)
    utils.spawn_walls(walls, MAP)
    portal1, portal2 = utils.spawn_portal(MAP)
    utils.spawn_walls(walls, MAP)
    CURRENT_DIRECTION = "r"
    wanted_direction = "r"
    snake = [(10, 1), (11, 1)]
    corner_safe = {(10, 1): "r", (11, 1): "r"}
    sweet = utils.spawn_sweet(SIZE, snake, walls)
    alive = True
    running = True


def draw_score(points: int, highscore: int):
    text = font.render(f"{points} HIGSCORE: {highscore}", True, "blue")
    screen.blit(text,
                (0, 0))

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

def draw_sweet():
    draw_picture(sweet_image, sweet[0], sweet[1])

def save_corner(pos, dir_before_move: str):
    global CURRENT_DIRECTION
    if dir_before_move != CURRENT_DIRECTION:
        corner_safe[pos] = f"{dir_before_move}{CURRENT_DIRECTION}"
    else:
        corner_safe[pos] = CURRENT_DIRECTION
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
    if (head_x := head[0]) != 1920 // SIZE - 1:
        snake.append((head_x + 1, head[1]))
        save_corner((head_x, head[1]), dir_before_move)
    else:
        snake.append((0, head[1]))
        save_corner((0, head[1]), dir_before_move)


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
    if (head_x := head[0]) != 0:
        snake.append((head_x - 1, head[1]))
        save_corner((head_x, head[1]), dir_before_move)
    else:
        snake.append((1920 // SIZE, head[1]))
        save_corner((1920 // SIZE, head[1]), dir_before_move)

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
    if (head_y := head[1]) != 1080 // SIZE - 1:
        snake.append((head[0], head_y + 1))
        save_corner((head[0], head_y), dir_before_move)
    else:
        snake.append((head[0], 0))
        save_corner((head[0], 0), dir_before_move)


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
    if (head_y := head[1]) != 0:
        snake.append((head[0], head_y - 1))
        save_corner((head[0], head_y), dir_before_move)
    else:
        snake.append((head[0], 1080 // SIZE))
        save_corner((head[0], 1080 // SIZE), dir_before_move)
def add_body_part():
    global CURRENT_DIRECTION
    snake.append(sweet)


def check_sweet() -> bool:
    return snake[-1] == sweet

def draw_picture(image, x, y):
    screen.blit(image, (x * SIZE, y * SIZE))

def draw_snake_head():
    if CURRENT_DIRECTION == "r":
        draw_picture(snake_head_l, snake[-1][0], snake[-1][1])
        return
    if CURRENT_DIRECTION == "d":
        draw_picture(snake_head_d, snake[-1][0], snake[-1][1])
        return
    if CURRENT_DIRECTION == "l":
        draw_picture(snake_head_r, snake[-1][0], snake[-1][1])
        return
    if CURRENT_DIRECTION == "u":
        draw_picture(snake_head_u, snake[-1][0], snake[-1][1])
        return


def draw_snake_tail_part(x, y):
    if (position := (x, y)) not in corner_safe:
        return
    rotation = corner_safe[position]
    last_snake_piece = position == snake[0]

    if last_snake_piece:
        #SORRY :( ber der code spart ein paat if abfragen weil man jetzt nur aufs ende von der rotation schauen muss
        match rotation[-1]:
            case "r":             # rotation in ("r" "ur" "dr")
                draw_picture(snake_end_r, x, y)
            case "l":
                draw_picture(snake_end_l, x, y)
            case "u":
                draw_picture(snake_end_u, x, y)
            case "d":
                draw_picture(snake_end_d, x, y)
    else:
        match rotation:
            case "r" | "l":
                draw_picture(snake_part_rl, x, y)
            case "u" | "d":
                draw_picture(snake_part_ud, x, y)
            case "rd" | "ul":
                draw_picture(snake_corner_dr, x, y)
            case "dr" | "lu":
                draw_picture(snake_corner_ul, x, y)
            case "ru" | "dl":
                draw_picture(snake_corner_ur, x, y)
            case "ur" | "ld":
                draw_picture(snake_corner_dl, x, y)

    keys_to_delete = [key for key in corner_safe.keys() if key not in snake]
    for i in keys_to_delete:
        corner_safe.pop(i)

def draw_snake_tail():
    for row_count, row in enumerate(snake):
        draw_snake_tail_part(row[0], row[1])

def draw_snake():
    draw_snake_head()
    draw_snake_tail()

def draw_walls():
    for row_count, row in enumerate(walls):
        draw_picture(wall_part, row[0], row[1])

def draw_portals():
    draw_picture(portal_image, portal1[0], portal1[1])
    draw_picture(portal_image, portal2[0], portal2[1])

def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()
def game_loop(map_str):
    highscore_set = False
    global running
    global alive
    global wanted_direction
    score = 0
    global sweet
    global speed
    init(map_str)
    highscore = utils.get_highscore(map_str)
    current_highscore = highscore
    speed_count = 0
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
            wanted_direction = pressed_direction_keys_queue.popleft()
            if wanted_direction != last_direction:
                alive = move(wanted_direction)
            last_direction = wanted_direction

        if alive:
            # fill the screen with a color to wipe away anything from last frame
            screen.fill("black")
            draw_walls()
            draw_portals()
            draw_sweet()
            draw_snake()

            if check_sweet():
                play_sound(eat_sound)
                score += 1
                add_body_part()
                sweet = utils.spawn_sweet(SIZE, snake, walls)
                if score > highscore:
                    highscore = score
                    if not highscore_set:
                        play_sound(beat_highscore_sound)
                        highscore_set = True

            draw_score(score, highscore)
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
            clock.tick(10)  # limits FPS to 60
            speed_count = 0

def draw_mini_map(map_name, start_pos):
    mini_size = 10
    map = utils.get_map(map_name)
    my_walls = list()
    utils.spawn_walls(my_walls, map)
    wall_part_mini = pygame.transform.scale(wall_part, (mini_size, mini_size))
    portal_image_mini = pygame.transform.scale(portal_image, (mini_size, mini_size))
    portal1, portal2 = utils.spawn_portal(map)
    for row_count, row in enumerate(my_walls):
        screen.blit(wall_part_mini, (start_pos[0] + row[0] * mini_size, start_pos[1] + row[1] * mini_size))
    screen.blit(portal_image_mini, (start_pos[0] + portal1[0] * mini_size, start_pos[1] + portal1[1] * mini_size))
    screen.blit(portal_image_mini, (start_pos[0] + portal2[0] * mini_size, start_pos[1] + portal2[1] * mini_size))
def intro():
    global screen
    global font
    blink_count = 0
    highscore_map_1 = utils.get_highscore("map1.csv")
    highscore_map_2 = utils.get_highscore("map2.csv")
    text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
    text_rect = text.get_rect(center=(1920 / 2, 100))
    map1_text = font.render(f"(1) Highscore: {highscore_map_1}", True, "white")
    map2_text = font.render(f"(2)Highscore: {highscore_map_2}", True, "white")
    map1_text_rect = map1_text.get_rect()
    map2_text_rect = map2_text.get_rect()
    map1_text_rect.center = (520, 780)
    map2_text_rect.center = (1400, 780)
    while intro:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_1]:
                play_sound(click_sound)
                return "map1.csv"
            if keys[pygame.K_2]:
                play_sound(click_sound)
                return "map2.csv"
            if keys[pygame.K_DELETE]:
                return
        screen.fill("black")
        if blink_count < 10:
            text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
        else:
            text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "red")
        screen.blit(text,
                    text_rect)
        draw_mini_map("map1.csv", (200, 360))
        draw_mini_map("map1.csv", (1080, 360))
        screen.blit(map1_text, map1_text_rect)
        screen.blit(map2_text, map2_text_rect)
        pygame.display.update()
        blink_count += 1
        if blink_count == 20:
            blink_count = 0
        clock.tick(20)

if __name__ == "__main__":
    while True:
        map = intro()
        if not map:
            break
        game_loop(map)
    pygame.quit()
