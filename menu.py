import pygame as pg
import menu_assets as ma
import snake.snake_assets as sa
import utils
import snake.snake_view as sv

CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
pg.mouse.set_visible(False)


def play_sound(sound):
    pg.mixer.Sound.play(sound)
    pg.mixer.music.stop()


def draw_mini_map(map_name, mini_size=18) -> pg.Surface:
    """
    Draw a mini-map for the menu
    :param map_name: name of the map
    :param start_pos: where to place the mini-map on the screen
    :param mini_size: Size of a cell
    """
    map_list = utils.get_map(map_name)
    game_board = sv.sc.GameBoard(map_list)

    mini_map_surface = pg.Surface(((game_board.dim.x + 2) * mini_size, (game_board.dim.y + 2) * mini_size))
    mini_map_surface.fill("darkorchid4")
    mini_map_surface.fill("grey8", (mini_size, mini_size, game_board.dim.x * mini_size, game_board.dim.y * mini_size))

    wall_part_mini = pg.transform.scale(ma.wall_image, (mini_size, mini_size))
    portal_images_mini = [pg.transform.scale(image, (mini_size, mini_size)) for image in ma.portal_images.values()]

    for wall_pos in game_board.walls:
        mini_map_surface.blit(wall_part_mini, ((wall_pos.x + 1) * mini_size, (wall_pos.y + 1) * mini_size))
    for portal_cell in game_board.portals.values():
        mini_map_surface.blit(portal_images_mini[portal_cell.subtype - 1], ((portal_cell.pos.x + 1) * mini_size, (portal_cell.pos.y + 1) * mini_size))

    return mini_map_surface


def intro():
    map_names = utils.get_all_map_names()
    selected_map_nr = 0
    selected_map_name = map_names[selected_map_nr]

    def switch_map_to(map_name: str):
        SCREEN.fill("black")
        highscore = utils.get_highscore(map_name)["score"]
        winner_map_1 = utils.get_highscore(map_name)["name"]
        text = ma.font.render("PRESS 1 FOR SINGLE- OR 2 FOR TWO-PLAYER", True, "blue")
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        map_text = ma.font.render(f"[{map_name}]  -  Highscore: {highscore}  -  Winner: {winner_map_1}", True, "white")
        map_text_rect = map_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        mini_map_surface = draw_mini_map(map_name)
        SCREEN.blit(mini_map_surface, mini_map_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        SCREEN.blit(text, text_rect)
        SCREEN.blit(map_text, map_text_rect)

    switch_map_to(selected_map_name)

    while intro:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None, None
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_ESCAPE, pg.K_DELETE):
                    return None, None

                elif event.key in (pg.K_LEFT, pg.K_RIGHT):
                    if event.key == pg.K_LEFT:
                        selected_map_nr -= 1
                    else:
                        selected_map_nr += 1
                    play_sound(sa.eat_sound)
                    selected_map_nr %= len(map_names)
                    selected_map_name = map_names[selected_map_nr]
                    switch_map_to(selected_map_name)

                elif event.key == pg.K_1:
                    play_sound(ma.click_sound)
                    return selected_map_name, False
                elif event.key == pg.K_2:
                    play_sound(ma.click_sound)
                    return selected_map_name, True

        pg.display.update()
        CLOCK.tick(20)


def new_highscore_dialog(map_name: str, game: sv.sc.Game):
    """
    Open dialog to enter name and message
    """
    old_winner = utils.get_highscore(map_name)["name"]
    old_message = utils.get_highscore(map_name)["message"]

    highscore_msg_popup = pg.Surface((1200, 700))
    highscore_msg_popup.fill((30, 230, 30))
    highscore_msg_popup.fill((30, 30, 30), (50, 50, 1100, 600))
    highscore_msg_popup.blit(
        ma.font_small.render(f"Du hast einen neuen Highscore von {game.highscore} für diese map erreicht!", True,
                             "white"),
        (100, 100))
    highscore_msg_popup.blit(
        ma.font_small.render(f"{old_winner} hat dir eine Nachricht hinterlassen:", True, "white"),
        (100, 150))
    highscore_msg_popup.blit(ma.font_small.render(f"\"{old_message}\"", True, "salmon"), (100, 225))
    highscore_msg_popup.blit(ma.font_small.render("Dein Name:", True, "white"), (100, 300))
    input_box1 = utils.InputBox(100, 350, 200, 32, active=True, max_len=12, text="Noob")

    highscore_msg_popup.blit(ma.font_small.render("Deine Nachricht:", True, "white"), (100, 400))
    input_box2 = utils.InputBox(100, 450, 1000, 32, max_len=64, text="Ich bin ein Noob")

    highscore_msg_popup.blit(ma.font_small.render("- drücke die Strg/Ctrl Taste um fortzufahren -", True, "white"),
                             (100, 550))

    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                elif event.key in (pg.K_LCTRL, pg.K_RCTRL):
                    done = True
            for box in input_boxes:
                box.handle_event(event)

        # for box in input_boxes:
        # box.update()

        SCREEN.blit(highscore_msg_popup, (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 400))
        for box in input_boxes:
            box.draw(highscore_msg_popup)

        pg.display.flip()
        CLOCK.tick(30)

    name = input_box1.text
    message = input_box2.text
    utils.save_highscore(map_name, game.highscore, name, message)


def winner_dialog(winner: str):
    """
    Open dialog showing who as won
    """

    text = ma.font.render(f"{winner}", True, "red")
    SCREEN.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                elif event.key == pg.K_RETURN:
                    done = True

        pg.display.flip()
        CLOCK.tick(30)


if __name__ == "__main__":

    while True:

        map_name1, two_players1 = intro()
        if not map_name1:
            break

        map_list1 = utils.get_map(map_name1)
        map_highscore1 = utils.get_highscore(map_name1)["score"]
        game1 = sv.sc.Game(map_list1, map_highscore1, two_players=two_players1)
        game_view1 = sv.GameView(SCREEN, CLOCK, game1)
        winner = game_view1.game_loop()

        if not two_players1:
            if game1.highscore_changed:
                new_highscore_dialog(map_name1, game1)
        else:
            winner_dialog(winner)

        CLOCK.tick(30)





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