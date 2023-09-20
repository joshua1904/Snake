# Example file showing a basic pygame "game loop"
import time
import random
import pygame
import csv

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True
SIZE = 20
snake = [(10, 0), (11, 0)]
speed = False
CURRENT_DIRECTION = "r"
wanted_direction = "r"
alive = True
points = 0
font = pygame.font.SysFont("comicsansms", 72)
walls = list()

def get_map():
    with open("map.csv", "r") as f:
        return list(csv.reader(f, delimiter=";"))

MAP = get_map()
def draw_score(points: int):
    text = font.render(str(points), True, "blue")
    screen.blit(text,
                (0, 0))


def spawn_portal() -> tuple:
    for row_counter, row in enumerate(MAP):
        if "2" in row:
           portal1 = (row.index("2"), row_counter)
        if "3" in row:
            portal2 = (row.index("3"), row_counter)
    return portal1, portal2
portal1, portal2 = spawn_portal()

def spawn_walls():
    for row_counter, row in enumerate(MAP):
        for field_counter, field in enumerate(row):
            if field == "1":
                walls.append((field_counter, row_counter))

spawn_walls()
def reset():
    global snake
    global points
    global wanted_direction
    global CURRENT_DIRECTION
    wanted_direction = "r"
    CURRENT_DIRECTION = "r"
    points = 0
    snake = [(10, 0), (11, 0)]
    return True
def spawn_sweet():
    sweet_x = random.randint(1, 999 // SIZE )
    sweet_y = random.randint(1, 999 // SIZE)
    if (sweet_xy := (sweet_x, sweet_y)) not in snake and sweet_xy not in walls:
        return sweet_xy
    else:
        return spawn_sweet()
sweet = spawn_sweet()
def move(dir: str):
    running = True
    if dir == "r":
        running = move_right()
    if dir == "u":
        running = move_up()
    if dir == "d":
       running =  move_down()
    if dir == "l":
        running = move_left()

    if running:
        if snake.count(snake[-1]) > 1 or list(walls).count(snake[-1]) == 1:
            return False
        return True
    return False

def draw_sweet():
    pygame.draw.rect(screen, "green", pygame.Rect(sweet[0] * SIZE, sweet[1] * SIZE, SIZE, SIZE))


def move_right():
    global CURRENT_DIRECTION
    if CURRENT_DIRECTION == "l":
        return move_left()
    CURRENT_DIRECTION = "r"
    head = snake[len(snake) - 1]
    snake.pop(0)
    if head == portal1:
        snake.append((portal2[0] + 1, portal2[1]))
        return True
    if head == portal2:
        snake.append((portal1[0] + 1, portal1[1]))
        return True
    if (head_x := head[0]) != 1000 // SIZE - 1:
        snake.append((head_x + 1, head[1]))
        return True
    else: 
        return False


def move_left():
    global CURRENT_DIRECTION
    if CURRENT_DIRECTION == "r":
        return move_right()
    CURRENT_DIRECTION = "l"
    head = snake[- 1]
    snake.pop(0)
    if head == portal1:
        snake.append((portal2[0] - 1, portal2[1]))
        return True
    if head == portal2:
        snake.append((portal1[0] - 1, portal1[1]))
        return True
    if (head_x := head[0]) != 0:
        snake.append((head_x - 1, head[1]))
        return True
    else:
        return False
def move_down():
    global CURRENT_DIRECTION
    if CURRENT_DIRECTION == "u":
        return move_up()
    CURRENT_DIRECTION = "d"
    head = snake[len(snake) - 1]
    snake.pop(0)
    if head == portal1:
        snake.append((portal2[0], portal2[1] + 1))
        return True
    if head == portal2:
        snake.append((portal1[0], portal1[1] + 1))
        return True
        return True
    if (head_y := head[1]) != 1000 // SIZE - 1:
        snake.append((head[0], head_y + 1))
        return True
    else:
        return False

def move_up():
    global CURRENT_DIRECTION
    if CURRENT_DIRECTION == "d":
        return move_down()
    CURRENT_DIRECTION = "u"
    head = snake[len(snake) - 1]
    snake.pop(0)
    if head == portal1:
        snake.append((portal2[0], portal2[1] -1))
        return True
    if head == portal2:
        snake.append((portal1[0], portal1[1] - 1))
        return True
    if (head_y := head[1]) != 0:
        snake.append((head[0], head_y - 1))
        return True
    else:
        return False

def add_body_part():
    snake.append(sweet)


def check_sweet() -> bool:
    return snake[len(snake) - 1] == sweet


def draw_rects():
    for row_count, row in enumerate(snake):
        pygame.draw.rect(screen, "red", pygame.Rect(row[0] * SIZE, row[1] * SIZE, SIZE, SIZE))
    for row_count, row in enumerate(walls):
        pygame.draw.rect(screen, "white", pygame.Rect(row[0] * SIZE, row[1] * SIZE, SIZE, SIZE))
    pygame.draw.rect(screen, "orange", pygame.Rect(portal1[0] * SIZE, portal1[1] * SIZE, SIZE, SIZE))
    pygame.draw.rect(screen, "orange", pygame.Rect(portal2[0] * SIZE, portal2[1] * SIZE, SIZE, SIZE))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        speed = keys[pygame.K_SPACE]
        if event.type == pygame.QUIT:
            running = False
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
            points += 1
            add_body_part()
            sweet = spawn_sweet()

        draw_score(points)
        # flip() the display to put your work on screen
        pygame.display.flip()
    if speed:
        clock.tick(20)
    else:
        clock.tick(10)  # limits FPS to 60
pygame.quit()
