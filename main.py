# Example file showing a basic pygame "game loop"
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
# r right l left u up d down (snake move direction
snake_part_rl = pygame.image.load("pictures/textures/tail-ew.bmp")
snake_part_ud = pygame.image.load("pictures/textures/tail-ns.bmp")

snake_corner_dr = pygame.image.load("pictures/textures/corner-se.bmp")
snake_corner_dl = pygame.image.load("pictures/textures/corner-sw.bmp")
snake_corner_ul = pygame.image.load("pictures/textures/corner-nw.bmp")
snake_corner_ur = pygame.image.load("pictures/textures/corner-ne.bmp")

snake_head_r = pygame.image.load("pictures/textures/head-e.bmp")
snake_head_u = pygame.image.load("pictures/textures/head-n.bmp")
snake_head_d = pygame.image.load("pictures/textures/head-s.bmp")
snake_head_l = pygame.image.load("pictures/textures/head-w.bmp")

snake_end_r = pygame.image.load("pictures/textures/head-e.bmp")
snake_end_u = pygame.image.load("pictures/textures/head-n.bmp")
snake_end_d = pygame.image.load("pictures/textures/head-s.bmp")
snake_end_l = pygame.image.load("pictures/textures/head-w.bmp")

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
    sweet = utils.spawn_sweet(SIZE, snake, walls)
    CURRENT_DIRECTION = "r"
    wanted_direction = "r"
    snake = [(10, 1), (11, 1)]
    corner_safe = {(10, 1): "r", (11, 1): "r"}
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


def move(dir: str):
    if dir == "r":
        running = move_right()
    if dir == "u":
        running = move_up()
    if dir == "d":
       running = move_down()
    if dir == "l":
        running = move_left()

    if running:
        if snake.count(snake[-1]) > 1 or walls.count(snake[-1]) > 1:
            return False
        return True
    return False

def draw_sweet():
    draw_picture(sweet_image, sweet[0], sweet[1])

def safe_corner(pos, dir_before_move: str):
    global CURRENT_DIRECTION
    if dir_before_move != CURRENT_DIRECTION:
        corner_safe[pos] = f"{dir_before_move}{CURRENT_DIRECTION}"
    else:
        corner_safe[pos] = CURRENT_DIRECTION
def move_right():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "l":
        return move_left()
    CURRENT_DIRECTION = "r"
    head = snake[len(snake) - 1]
    snake.pop(0)

    if head == portal1:
        snake.append((portal2[0] + 1, portal2[1]))
        safe_corner((portal2[0], portal2[1]), dir_before_move)
        return True
    if head == portal2:
        snake.append((portal1[0] + 1, portal1[1]))
        safe_corner((portal1[0], portal1[1]), dir_before_move)
        return True
    if (head_x := head[0]) != 1920 // SIZE - 1:
        snake.append((head_x + 1, head[1]))
        safe_corner((head_x, head[1]), dir_before_move)
        return True
    else: 
        return False


def move_left():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "r":
        return move_right()
    CURRENT_DIRECTION = "l"
    head = snake[- 1]
    snake.pop(0)

    if head == portal1:
        snake.append((portal2[0] - 1, portal2[1]))
        safe_corner((portal2[0], portal2[1]), dir_before_move)
        return True
    if head == portal2:
        snake.append((portal1[0] - 1, portal1[1]))
        safe_corner((portal1[0], portal1[1]), dir_before_move)
        return True
    if (head_x := head[0]) != 0:
        snake.append((head_x - 1, head[1]))
        safe_corner((head_x, head[1]), dir_before_move)
        return True
    else:
        return False
def move_down():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "u":
        return move_up()
    CURRENT_DIRECTION = "d"
    head = snake[- 1]
    snake.pop(0)

    if head == portal1:
        snake.append((portal2[0], portal2[1] + 1))
        safe_corner((portal2[0], portal2[1]), dir_before_move)
        return True
    if head == portal2:
        snake.append((portal1[0], portal1[1] + 1))
        safe_corner((portal1[0], portal1[1]), dir_before_move)
        return True
    if (head_y := head[1]) != 1080 // SIZE - 1:
        snake.append((head[0], head_y + 1))
        safe_corner((head[0], head_y), dir_before_move)
        return True
    else:
        return False

def move_up():
    global CURRENT_DIRECTION
    dir_before_move = CURRENT_DIRECTION
    if CURRENT_DIRECTION == "d":
        return move_down()
    CURRENT_DIRECTION = "u"
    head = snake[len(snake) - 1]
    snake.pop(0)

    if head == portal1:
        snake.append((portal2[0], portal2[1] -1))
        safe_corner((portal2[0], portal2[1]), dir_before_move)
        return True
    if head == portal2:
        snake.append((portal1[0], portal1[1] - 1))
        safe_corner((portal1[0], portal1[1]), dir_before_move)
        return True
    if (head_y := head[1]) != 0:
        snake.append((head[0], head_y - 1))
        safe_corner((head[0], head_y), dir_before_move)
        return True
    else:
        return False

def add_body_part():
    global CURRENT_DIRECTION
    snake.append(sweet)


def check_sweet() -> bool:
    return snake[len(snake) - 1] == sweet

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
    global CURRENT_DIRECTION
    if (position := (x, y)) not in corner_safe:
        return
    rotation = corner_safe[position]
    last_snake_piece = position == snake[0]
    if last_snake_piece:
        #SORRY :( ber der code spart ein paat if abfragen weil man jetzt nur aufs ende von der rotation schauen muss
        if len(rotation) < 1:
            r = rotation[1]
        if rotation == "r" :
            draw_picture(snake_end_r, x, y)
            return
        if rotation == "l":
            draw_picture(snake_end_l, x, y)
            return
        if rotation == "u":
            draw_picture(snake_end_u, x, y)
            return
        if rotation == "d":
            draw_picture(snake_end_d, x, y)
            return
        return
    if rotation == "r" or rotation == "l":
        draw_picture(snake_part_rl, x, y)
        return
    if rotation == "u" or rotation == "d":
        draw_picture(snake_part_ud, x, y)
        return
    if rotation == "rd" or rotation == "ul":
        draw_picture(snake_corner_dr, x, y)
        return
    if rotation == "dr" or rotation == "lu":
        draw_picture(snake_corner_ul, x, y)
    if rotation == "ru" or rotation == "dl":
        draw_picture(snake_corner_ur, x, y)
    if rotation == "ur" or rotation == "ld":
        draw_picture(snake_corner_dl, x, y)

    keys_to_delete = [key for key in corner_safe.keys() if key not in snake]
    for i in keys_to_delete:
        corner_safe.pop(i)

def draw_snake_tail():
    for row_count, row in enumerate(snake):
        draw_snake_tail_part(row[0], row[1])

def draw_rects():
    draw_snake_tail()
    draw_snake_head()
    for row_count, row in enumerate(walls):
        draw_picture(wall_part, row[0], row[1])
    draw_picture(portal_image, portal1[0], portal1[1])
    draw_picture(portal_image, portal2[0], portal2[1])

def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()
def game_loop(map_str):
    global running
    global alive
    global wanted_direction
    score = 0
    global sweet
    global speed
    init(map_str)
    highscore = utils.get_highscore(map_str)
    current_highscore = highscore
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            speed = keys[pygame.K_SPACE]
            if keys[pygame.K_HASH]:
                alive = reset()
            if keys[pygame.K_LEFT]:
                wanted_direction = "l"
                break
            if keys[pygame.K_RIGHT]:
                wanted_direction = "r"
                break
            if keys[pygame.K_UP]:
                wanted_direction = "u"
                break
            if keys[pygame.K_DOWN]:
                wanted_direction = "d"
                break

        # move_right()
        # fill the screen with a color to wipe away anything from last frame
        if alive:
            screen.fill("black")
            alive = move(wanted_direction)
            draw_rects()
            draw_sweet()
            if check_sweet():
                play_sound(eat_sound)
                score += 1
                add_body_part()
                sweet = utils.spawn_sweet(SIZE, snake, walls)
                if score > highscore:
                    highscore = score

            draw_score(score, highscore)
            # flip() the display to put your work on screen
            pygame.display.flip()
        else:
            play_sound(damage_sound)
            if highscore > current_highscore:
                utils.set_highscore(map_str, highscore)
            return
        if speed:
            clock.tick(20)
        else:
            clock.tick(10)  # limits FPS to 60

def intro():
    global screen
    global font
    blink_count = 0
    highscore_map_1 = utils.get_highscore("map1.csv")
    highscore_map_2 = utils.get_highscore("map2.csv")
    text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
    text_rect = text.get_rect(center=(1920 / 2, 100))
    map1 = pygame.image.load("pictures/maps/ajz_map.png")
    map1 = pygame.transform.scale(map1, (16 * 50, 9 * 50))
    map2 = pygame.image.load("pictures/maps/empty_map.png")
    map2 = pygame.transform.scale(map2, (16 * 50, 9 * 50))
    map1_rect = map1.get_rect()
    map2_rect = map2.get_rect()
    map1_rect.center = (1920 // 4, 1080 // 2)
    map2_rect.center = (3 * 1920 // 4, 1080 // 2)
    map1_text = font.render(f"(1) Highscore: {highscore_map_1}", True, "black")
    map2_text = font.render(f"(2)Highscore: {highscore_map_2}", True, "black")
    map1_text_rect = map1_text.get_rect()
    map2_text_rect = map2_text.get_rect()
    map1_text_rect.midtop = (map1_rect.centerx, map1_rect.bottom + 10)
    map2_text_rect.midtop = (map2_rect.centerx, map2_rect.bottom + 10)
    while intro:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys[pygame.K_1]:
                return "map1.csv"
            if keys[pygame.K_2]:
                return "map2.csv"
            if keys[pygame.K_DELETE]:
                return
        screen.fill("white")
        if blink_count < 10:
            text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
        else:
            text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "red")
        screen.blit(text,
                    text_rect)
        screen.blit(map1, map1_rect)
        screen.blit(map2, map2_rect)
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
