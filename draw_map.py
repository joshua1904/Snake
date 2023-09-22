import random
import time

import pygame
import csv

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
walls = list()
removed_walls = list()
SIZE = 30

def draw_rect(x: int, y: int, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * SIZE, y * SIZE, SIZE, SIZE))
def get_map():
    with open("map1.csv", "r") as f:
        return list(csv.reader(f, delimiter=";"))


def add_to_map():
    for row_counter, row in enumerate(MAP):
        if "2" in row:
            row[row.index("2")] = "0"
        if "3" in row:
            row[row.index("3")] = "0"
        for field_counter, field in enumerate(row):
            pos = (field_counter, row_counter)
            if pos in removed_walls:
                MAP[row_counter][field_counter] = "0"
            if pos in walls:
                MAP[row_counter][field_counter] = "1"
            if pos == portal1:
                MAP[row_counter][field_counter] = "2"
            if pos == portal2:
                MAP[row_counter][field_counter] = "3"

    with open("map1.csv", "w") as f:
        for row in MAP:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(row)

MAP = get_map()
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
def draw_rects():
    for row_count, row in enumerate(walls):
        draw_rect(row[0], row[1], "white")
    if portal1:
        draw_rect(portal1[0], portal1[1], "orange")
    if portal2:
        draw_rect(portal2[0], portal2[1], "orange")

def draw(pos: tuple, delete=False):
    global portal1, portal2
    grid_pos = (pos[0] // SIZE, pos[1] // SIZE)
    if not delete:
        if not portal1:
            portal1 = grid_pos
            add_to_map()
            return
        if not portal2:
            portal2 = grid_pos
            add_to_map()
            return
        if grid_pos not in walls:
            walls.append(grid_pos)
    else:
        if grid_pos == portal1:
            portal1 = None
            return
        if grid_pos == portal2:
            portal2 = None
            return
        if grid_pos in walls:
            walls.remove(grid_pos)
            removed_walls.append(grid_pos)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_DELETE]:
            running = False
        if mouse[0]:
            pos = pygame.mouse.get_pos()
            draw(pos)
        if mouse[2]:
            pos = pygame.mouse.get_pos()
            draw(pos, delete=True)
    # move_right()
    # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        # flip() the display to put your work on screen
        draw_rects()
        pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
pygame.quit()
add_to_map()