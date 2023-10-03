from snake.assets import *
from snake import snake
import utils

screen = pygame.display.set_mode((0, 0), FULLSCREEN)
def draw_mini_map(map_name, start_pos):
    mini_size = 10
    map = utils.get_map(map_name)
    my_walls = list()
    utils.spawn_walls(my_walls, map)
    wall_part_mini = pygame.transform.scale(wall_image, (mini_size, mini_size))
    portal_image_mini = pygame.transform.scale(portal_image, (mini_size, mini_size))
    portal1, portal2 = utils.spawn_portal(map)
    for row_count, row in enumerate(my_walls):
        screen.blit(wall_part_mini, (start_pos[0] + row[0] * mini_size, start_pos[1] + row[1] * mini_size))
    screen.blit(portal_image_mini, (start_pos[0] + portal1[0] * mini_size, start_pos[1] + portal1[1] * mini_size))
    screen.blit(portal_image_mini, (start_pos[0] + portal2[0] * mini_size, start_pos[1] + portal2[1] * mini_size))

def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()
def intro():
    blink_count = 0
    highscore_map_1 = utils.get_highscore("map1.csv")
    highscore_map_2 = utils.get_highscore("map3.csv")
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
                return "maps/map1.csv"
            if keys[pygame.K_2]:
                play_sound(click_sound)
                return "maps/map3.csv"
            if keys[pygame.K_DELETE]:
                return
        screen.fill("black")
        if blink_count < 10:
            text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
        else:
            text = font.render("PRESS 1 OR 2 TO START THE GAME", True, "red")
        screen.blit(text,
                    text_rect)
        draw_mini_map("maps/map1.csv", (200, 360))
        draw_mini_map("maps/map3.csv", (1080, 360))
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
        snake.game_loop(map, screen)