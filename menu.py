import pygame as pg
import menu_assets as ma
import utils
import snake.snake_view as sv

CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
pg.mouse.set_visible(False)


COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')


class InputBox:

    def __init__(self, x, y, w, h, text='', active=False, max_len=100):
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.active = active
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        self.txt_surface = ma.font_small.render(text, True, self.color)
        self.max_len = max_len
        self.bg_color = pg.Color(30, 30, 30)

    def handle_event(self, event):
        # if event.type == pg.MOUSEBUTTONDOWN:
        #     # If the user clicked on the input_box rect.
        #     if self.rect.collidepoint(event.pos):
        #         # Toggle the active variable.
        #         self.active = not self.active
        #     else:
        #         self.active = False
        #     # Change the current color of the input box.

        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_UP, pg.K_DOWN, pg.K_RETURN):
                self.active = not self.active
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

            if self.active:
                # if event.key == pg.K_RETURN:
                #     print(self.text)
                #     self.text = ''
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    char = event.unicode
                    if ((char.isascii() and char.isalnum()) or char in '!?.,-()<>') and len(self.text) <= self.max_len:
                        self.text += char

                # Re-render the text.
                self.txt_surface = ma.font_small.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        pg.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def draw_mini_map(map_name, start_pos, mini_size=10):
    """
    Draw a mini-map for the menu
    :param map_name: name of the map
    :param start_pos: where to place the mini-map on the screen
    :param mini_size: Size of a cell
    """
    map_list = utils.get_map(map_name)

    game_board = sv.sc.GameBoard(map_list)

    wall_part_mini = pg.transform.scale(ma.wall_image, (mini_size, mini_size))
    portal_images_mini = [pg.transform.scale(image, (mini_size, mini_size)) for image in ma.portal_images.values()]

    for wall_pos in game_board.walls:
        SCREEN.blit(wall_part_mini, (start_pos[0] + wall_pos.x * mini_size, start_pos[1] + wall_pos.y * mini_size))
    for portal_cell in game_board.portals.values():
        SCREEN.blit(portal_images_mini[portal_cell.subtype - 1], (start_pos[0] + portal_cell.pos.x * mini_size, start_pos[1] + portal_cell.pos.y * mini_size))


def play_sound(sound):
    pg.mixer.Sound.play(sound)
    pg.mixer.music.stop()


def intro():
    SCREEN.fill("black")
    highscore_map_1 = utils.get_highscore("map1")["score"]
    highscore_map_2 = utils.get_highscore("map3")["score"]
    winner_map_1 = utils.get_highscore("map1")["name"]
    winner_map_2 = utils.get_highscore("map3")["name"]
    text = ma.font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
    text_rect = text.get_rect(center=(1920 / 2, 100))
    map1_text = ma.font.render(f"(1) Highscore: {highscore_map_1} ({winner_map_1})", True, "white")
    map2_text = ma.font.render(f"(2) Highscore: {highscore_map_2} ({winner_map_2})", True, "white")
    map1_text_rect = map1_text.get_rect()
    map2_text_rect = map2_text.get_rect()
    map1_text_rect.center = (520, 780)
    map2_text_rect.center = (1400, 780)
    draw_mini_map("map1", (200, 360))
    draw_mini_map("map3", (1080, 360))
    text = ma.font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
    SCREEN.blit(text, text_rect)
    SCREEN.blit(map1_text, map1_text_rect)
    SCREEN.blit(map2_text, map2_text_rect)

    while intro:
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

            if keys[pg.K_1]:
                play_sound(ma.click_sound)
                return "map1"
            if keys[pg.K_2]:
                play_sound(ma.click_sound)
                return "map3"
            if keys[pg.K_DELETE]:
                return

        pg.display.update()
        CLOCK.tick(20)


if __name__ == "__main__":

    while True:

        map_name = intro()
        if not map_name:
            break

        map_list = utils.get_map(map_name)
        map_highscore = utils.get_highscore(map_name)["score"]
        game = sv.sc.Game(map_list, map_highscore)
        game_view = sv.GameView(SCREEN, CLOCK, game)
        game_view.game_loop()

        if game.highscore_changed:

            old_winner = utils.get_highscore(map_name)["name"]
            old_message = utils.get_highscore(map_name)["message"]

            highscore_msg_popup = pg.Surface((800, 700))
            highscore_msg_popup.fill((230, 30, 30))
            highscore_msg_popup.fill((30, 30, 30), (50, 50, 700, 600))
            highscore_msg_popup.blit(
                ma.font_small.render("Du hast einen neuen Highscore für diese map erreicht!", True, "white"),
                (100, 100))
            highscore_msg_popup.blit(
                ma.font_small.render(f"{old_winner} hat dir eine Nachricht hinterlassen:", True, "white"),
                (100, 150))
            highscore_msg_popup.blit(ma.font_small.render(f"\"{old_message}\"", True, "white"), (100, 200))
            highscore_msg_popup.blit(ma.font_small.render("Dein Name:", True, "white"), (100, 250))
            input_box1 = InputBox(100, 300, 200, 32, active=True, max_len=12, text="Noob")

            highscore_msg_popup.blit(ma.font_small.render("Deine Nachricht:", True, "white"), (100, 350))
            input_box2 = InputBox(100, 400, 600, 32, max_len=36, text="Ich bin ein Noob")

            highscore_msg_popup.blit(ma.font_small.render("- drücke die Strg/Ctrl Taste um fortzufahren -", True, "white"), (100, 500))

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

                SCREEN.blit(highscore_msg_popup, (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2 - 400))
                for box in input_boxes:
                    box.draw(highscore_msg_popup)

                pg.display.flip()
                CLOCK.tick(30)

            name = input_box1.text
            message = input_box2.text
            utils.save_highscore(map_name, game.highscore, name, message)





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