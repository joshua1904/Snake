import pygame as pg
import menu_assets as ma
import utils
import snake.snake_view as sv

CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = ma.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = ma.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
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
    highscore_map_1 = utils.get_highscore("map1")
    highscore_map_2 = utils.get_highscore("map3")
    text = ma.font.render("PRESS 1 OR 2 TO START THE GAME", True, "blue")
    text_rect = text.get_rect(center=(1920 / 2, 100))
    map1_text = ma.font.render(f"(1) Highscore: {highscore_map_1}", True, "white")
    map2_text = ma.font.render(f"(2)Highscore: {highscore_map_2}", True, "white")
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