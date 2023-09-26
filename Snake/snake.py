# Example file showing a basic pygame "game loop"
import collections
from Snake import utils
from Snake.assets import *

# pygame setup

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
walls = list()

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
    if (head_x := head[0]) < 1920 // SIZE - 1:
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
    if (head_x := head[0]) >= 1:
        snake.append((head_x - 1, head[1]))
        save_corner((head_x, head[1]), dir_before_move)
    else:
        snake.append((1920 // SIZE - 1, head[1]))
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
    if (head_y := head[1]) <= 1080 // SIZE - 2:
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
    if (head_y := head[1]) >= 1:
        snake.append((head[0], head_y - 1))
        save_corner((head[0], head_y), dir_before_move)
    else:
        snake.append((head[0], 1080 // SIZE - 1))
        save_corner((head[0], 1080 // SIZE), dir_before_move)
def add_body_part():
    global CURRENT_DIRECTION
    snake.append(sweet)


def check_sweet() -> bool:
    return snake[-1] == sweet

def draw_picture(image, x, y, screen):
    screen.blit(image, (x * SIZE, y * SIZE))

def draw_snake_head(screen):
    if CURRENT_DIRECTION == "r":
        draw_picture(snake_head_l, snake[-1][0], snake[-1][1], screen)
        return
    if CURRENT_DIRECTION == "d":
        draw_picture(snake_head_d, snake[-1][0], snake[-1][1], screen)
        return
    if CURRENT_DIRECTION == "l":
        draw_picture(snake_head_r, snake[-1][0], snake[-1][1], screen)
        return
    if CURRENT_DIRECTION == "u":
        draw_picture(snake_head_u, snake[-1][0], snake[-1][1], screen)
        return


def draw_snake_tail_part(x, y, screen):
    if (position := (x, y)) not in corner_safe:
        return
    rotation = corner_safe[position]
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

    keys_to_delete = [key for key in corner_safe.keys() if key not in snake]
    for i in keys_to_delete:
        corner_safe.pop(i)

def draw_snake_tail(screen):
    for row_count, row in enumerate(snake):
        draw_snake_tail_part(row[0], row[1], screen)

def draw_snake(screen):
    draw_snake_head(screen)
    draw_snake_tail(screen)

def draw_walls(screen):
    for row_count, row in enumerate(walls):
        draw_picture(wall_part, row[0], row[1], screen)

def draw_portals(screen):
    draw_picture(portal_image, portal1[0], portal1[1], screen)
    draw_picture(portal_image, portal2[0], portal2[1], screen)

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
    init(map_str)
    highscore = utils.get_highscore(map_str)
    current_highscore = highscore
    speed_count = 0

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
        else:
            wanted_direction = pressed_direction_keys_queue.popleft()
            alive = move(wanted_direction)

        if alive:
            # fill the screen with a color to wipe away anything from last frame
            screen.fill("black")
            draw_walls(screen)
            draw_portals(screen)
            draw_sweet(screen)
            draw_snake(screen)

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
            clock.tick(10)  # limits FPS to 60
            speed_count = 0
