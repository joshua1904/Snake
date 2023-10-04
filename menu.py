import pygame
import menu_assets
import utils
import snake.snake_view as sv

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()


def draw_mini_map(map_name, start_pos, mini_size=10):
    """
    Draw a mini-map for the menu
    :param map_name: name of the map
    :param start_pos: where to place the mini-map on the screen
    :param mini_size: Size of a cell
    """
    map_list = utils.get_map(map_name)

    game_board = sv.sc.GameBoard(map_list)

    wall_part_mini = pygame.transform.scale(menu_assets.wall_image, (mini_size, mini_size))
    portal_images_mini = [pygame.transform.scale(image, (mini_size, mini_size)) for image in menu_assets.portal_images.values()]

    for wall_pos in game_board.walls:
        SCREEN.blit(wall_part_mini, (start_pos[0] + wall_pos.x * mini_size, start_pos[1] + wall_pos.y * mini_size))
    for portal_cell in game_board.portals.values():
        SCREEN.blit(portal_images_mini[portal_cell.subtype - 1], (start_pos[0] + portal_cell.pos.x * mini_size, start_pos[1] + portal_cell.pos.y * mini_size))


def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()


def intro():
    SCREEN.fill("black")
    highscore_map_1 = utils.get_highscore("map1")
    highscore_map_2 = utils.get_highscore("map3")
    text = menu_assets.font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
    text_rect = text.get_rect(center=(1920 / 2, 100))
    map1_text = menu_assets.font.render(f"(1) Highscore: {highscore_map_1}", True, "white")
    map2_text = menu_assets.font.render(f"(2)Highscore: {highscore_map_2}", True, "white")
    map1_text_rect = map1_text.get_rect()
    map2_text_rect = map2_text.get_rect()
    map1_text_rect.center = (520, 780)
    map2_text_rect.center = (1400, 780)
    draw_mini_map("map1", (200, 360))
    draw_mini_map("map3", (1080, 360))
    text = menu_assets.font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
    SCREEN.blit(text, text_rect)
    SCREEN.blit(map1_text, map1_text_rect)
    SCREEN.blit(map2_text, map2_text_rect)

    while intro:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if keys[pygame.K_1]:
                play_sound(menu_assets.click_sound)
                return "map1"
            if keys[pygame.K_2]:
                play_sound(menu_assets.click_sound)
                return "map3"
            if keys[pygame.K_DELETE]:
                return

        pygame.display.update()
        CLOCK.tick(20)


if __name__ == "__main__":

    while True:

        map_name = intro()
        if not map_name:
            break

        map_list = utils.get_map(map_name)
        map_highscore = utils.get_highscore(map_name)
        game = sv.sc.Game(map_list, map_highscore)
        game_view = sv.GameView(SCREEN, CLOCK, game)
        game_view.game_loop()

        if game.highscore_changed:
            utils.save_highscore(map_name, game.highscore)



# map_list = [[1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1],
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 'r', 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 5, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1]]