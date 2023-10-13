# Example file showing a basic pygame "game loop"
import copy
from tetris_assets import game_sound, font
import pygame
from tetris.pitch import PIXEL_MAP
from tetris.game_logic import GameLogic
from tetris_assets import highscore_json
import json

class TetrisView:
    def __init__(self, screen: pygame.surface, clock: pygame.time.Clock):
        self.screen_width = 1920
        self.screen_height = 720
        # pygame setup
        pygame.init()
        self.screen = screen
        self.clock = clock
        self.pixel_width = 40
        self.game_pitch_start_x = self.screen_width // 2 - (10 * self.pixel_width / 2)
        self.game_pitch_start_y = 200
        self.game_logic = GameLogic()
        game_sound.play(-1)

    def get_highscore(self):
        highscore = 0
        with open(highscore_json, "r") as f:
            highscore = json.load(f)
        if highscore == {}:
            return 0
        return highscore["value"]

    def set_highscore(self, score):
        with open(highscore_json) as f:
            json.dump({"value": score})


    def draw_score(self, screen, score: int, level: int):
        score = font.render(f"Score: {score}     Level: {level}", True, "white")
        score_rect = score.get_rect(center=(self.screen_width / 2, 100))
        screen.blit(score, score_rect)

    def draw_rect(self, screen, pixel: int, y: int, x: int):
        pygame.draw.rect(screen, PIXEL_MAP[pixel],
                         (self.game_pitch_start_x + x * self.pixel_width, self.game_pitch_start_y +
                          y * self.pixel_width, self.pixel_width, self.pixel_width), )

    def draw_pitch(self, screen):
        pygame.draw.rect(screen, "white", (self.game_pitch_start_x, self.game_pitch_start_y
                                           , self.pixel_width * 10, self.pixel_width * 20), 2)

    def draw_map(self):
        for row_count, row in enumerate(self.game_logic.pitch.pitch_list):
            for pixel_count, pixel in enumerate(row):
                if pixel != 0:
                    self.draw_rect(self.screen, pixel, row_count, pixel_count)

    def draw_form(self):
        color = self.game_logic.pitch.moving_form.get_color_int()
        for pixel in self.game_logic.pitch.moving_form.get_pixel_positions():
            self.draw_rect(self.screen, color, pixel[0], pixel[1])

    def draw_fake_form(self, screen, fake_form):
        for pixel in fake_form.get_pixel_positions():
            self.draw_rect(screen, 0, pixel[0], pixel[1])

    def draw_special_forms(self, screen, location: tuple, form):
        pygame.draw.rect(screen, "white", (
        location[0] * self.pixel_width, location[1] * self.pixel_width, self.pixel_width * 5, self.pixel_width * 5), 5)
        if form:
            fake_form_draw = copy.deepcopy(form)
            fake_form_draw.set_pos(location[0], location[1])
            color = fake_form_draw.get_color_int()
            for pixel in fake_form_draw.get_pixel_positions():
                pygame.draw.rect(screen, PIXEL_MAP[color], ((pixel[1] + 1) * self.pixel_width,
                                                            (pixel[0] + 1) * self.pixel_width, self.pixel_width,
                                                            self.pixel_width), 5)

    def game_loop(self):
        running = True
        count = 0
        control_time_count = 0
        direction = None
        no_movement = True
        current_level = self.game_logic.level
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.game_logic.rotate("down")
                    if event.key == pygame.K_UP:
                        self.game_logic.rotate("up")
                    if event.key == pygame.K_SPACE:
                        self.game_logic.change_form()
                    if event.key == pygame.K_LEFT:
                        direction = "left"
                        no_movement = False
                    if event.key == pygame.K_RIGHT:
                        direction = "right"
                        no_movement = False
                    if event.key == pygame.K_RCTRL:
                        self.game_logic.down_boost()
                        running = self.game_logic.game_round()
                        break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                        no_movement = True
                        direction = None
            if control_time_count % 7 == 0 or no_movement:
                control_time_count = 0
                if direction == "right":
                    self.game_logic.move_right()
                if direction == "left":
                    self.game_logic.move_left()
            if count == self.game_logic.get_speed():
                count = 0
                running = self.game_logic.game_round()

                # RENDER YOUR GAME HERE

                # flip() the display to put your work on screen

                spin = None
            if current_level < self.game_logic.level:
                current_level = self.game_logic.level
                count = 0
            count += 1
            control_time_count += 1
            self.screen.fill("black")

            self.draw_map()
            self.draw_fake_form(self.screen, self.game_logic.get_goal_position())
            self.draw_form()
            self.draw_pitch(self.screen)
            self.draw_special_forms(self.screen, (5, 5), self.game_logic.pitch.change_form)
            self.draw_special_forms(self.screen, (5, 10), self.game_logic.pitch.next_form)
            self.draw_score(self.screen, self.game_logic.score, self.game_logic.level)
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


p = TetrisView(pygame.display.set_mode((0, 0), pygame.FULLSCREEN), pygame.time.Clock())
p.game_loop()