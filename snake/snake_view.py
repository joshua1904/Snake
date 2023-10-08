"""
The front-end with pygame
"""
from collections import deque

import snake.snake_classes as sc
import snake.snake_assets as sa
import pygame as pg


def play_sound(sound):
    pg.mixer.Sound.play(sound)
    pg.mixer.music.stop()


class GameView:
    """
    The view of a single game
    """
    MIDDLE_PARTS = {
        'll': 'rl', 'rr': 'rl',
        'uu': 'ud', 'dd': 'ud',
        'rd': 'dr', 'ul': 'dr',
        'dr': 'ul', 'lu': 'ul',
        'ru': 'ur', 'dl': 'ur',
        'ur': 'dl', 'ld': 'dl'
    }

    def __init__(self, screen: pg.Surface, clock: pg.time.Clock,
                 game: sc.Game, cell_size=30, start_speed=10, inc_speed=False):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.clock = clock

        self.game = game
        self.cell_size = cell_size
        self.start_speed = start_speed
        self.inc_speed = inc_speed

        self.map_width_px = self.game.board.dim.x * self.cell_size
        self.map_height_px = self.game.board.dim.y * self.cell_size
        self.map_surface: pg.Surface        # the (immutable) background with walls and portals

        self.background_image = sa.wall_image
        self._init_map_surface()

    def _init_map_surface(self):
        """Prepare the map_surface"""
        self.map_surface = self.screen.copy()
        self.map_surface.fill("black")

        # Background with border
        border = pg.Surface((self.map_width_px + (2 * self.cell_size),
                             self.map_height_px + (2 * self.cell_size)))
        border.fill("darkorchid4")
        self.draw_to_board(border, -1, -1, self.map_surface)
        background_surface = self._create_background(self.background_image)
        self.draw_to_board(background_surface, 0, 0, self.map_surface)

        # Walls
        for wall_pos in self.game.board.walls:
            self.draw_to_board(sa.wall_image, wall_pos.x, wall_pos.y, self.map_surface)

        # Portals
        for portal_cell in self.game.board.portals.values():
            self.draw_to_board(sa.portal_images[portal_cell.subtype], portal_cell.pos.x, portal_cell.pos.y, self.map_surface)

    def _create_background(self, image: pg.image, tile_size=(360, 360), darker=90) -> pg.Surface:
        """
        Generate Background-Image
        :param image: the image to use for the background
        :param tile_size: how big the image should be scaled in pixels
        :param darker: r, g, b values to be subtracted from image (0-255)
        :return: the background surface (as big as the map)
        """
        scaled_image = pg.transform.smoothscale(image, tile_size)
        scaled_image.fill((darker, darker, darker), special_flags=pg.BLEND_RGB_SUB)
        background_surface = pg.Surface((self.map_width_px, self.map_height_px))
        for x in range(0, self.map_width_px // tile_size[0] + 1):
            for y in range(0, self.map_height_px // tile_size[1] + 1):
                background_surface.blit(scaled_image, (x * tile_size[0], y * tile_size[1]))
        return background_surface

    def draw_to_board(self, image: pg.image, x: int, y: int, surface: pg.Surface):
        """
        :param image: the image to draw
        :param x: x-Coord. on the board (in cells)
        :param y: y-Coord. on the board (in cells)
        :param surface: the surface to draw to
        """
        surface.blit(image, (x * self.cell_size + self.screen_width // 2 - self.map_width_px // 2,
                             y * self.cell_size + self.screen_height // 2 - self.map_height_px // 2))

    def draw_snake(self, snake: sc.Snake):
        """
        Draw the snake
        end -> parts -> head
        """
        head_pos = snake.positions[-1]
        head_dir = snake.directions[-1]
        end_pos = snake.positions[0]
        end_dir = snake.directions[1]

        # Draw head
        img = sa.snake_head[head_dir] if not snake.evil else sa.snake_head_2[head_dir]
        self.draw_to_board(img, head_pos.x, head_pos.y, self.screen)

        # Draw tail
        img = sa.snake_end[end_dir] if not snake.evil else sa.snake_end_2[end_dir]
        self.draw_to_board(img, end_pos.x, end_pos.y, self.screen)

        # Draw middle parts
        img_list = sa.snake_part if not snake.evil else sa.snake_part_2
        for i, part_pos in enumerate(snake.positions):
            if i in range(1, len(snake.positions) - 1):
                part_dir = snake.directions[i]
                part_next_dir = snake.directions[i + 1]
                corner_id = GameView.MIDDLE_PARTS[part_dir + part_next_dir]
                self.draw_to_board(img_list[corner_id], part_pos.x, part_pos.y, self.screen)

    def draw_map(self):
        """Draw the background and map to the screen"""
        self.screen.blit(self.map_surface, (0, 0))

    def draw_sweet(self):
        """Draw the sweet on the screen"""
        sweet = self.game.sweet
        self.draw_to_board(sa.sweet_image, sweet.pos.x, sweet.pos.y, self.screen)

    def draw_score(self):
        """Draw the current score"""
        text = sa.font.render(f"{self.game.score} HIGHSCORE: {self.game.highscore}", True, "blue")
        self.screen.blit(text, (30, 30))

    def draw_two_player_score(self):
        """Draw the current score: two player"""
        text_good = sa.font.render(f"GRÜN:  {self.game.score_good}  /  {self.game.max_score}", True, "chartreuse3")
        text_evil = sa.font.render(f"LILA:  {self.game.score_evil}  /  {self.game.max_score}", True, "magenta3")
        self.screen.blit(text_good, (60, 30))
        self.screen.blit(text_evil, (self.screen_width - text_evil.get_width() - 60, 30))

    def game_loop(self):
        """the main loop"""

        # allow only certain events (no mouse)
        pg.event.set_allowed((pg.QUIT, pg.KEYDOWN, pg.KEYUP))

        # save pressed keys in queue
        pressed_direction_keys_queue = deque(list())
        speed = False
        last_direction = self.game.snake.directions[-1]     
        current_direction = last_direction
        move_event = None
        speed_key = pg.K_SPACE

        # Snake 2
        pressed_direction_keys_queue_2 = None
        speed_2 = False
        last_direction_2 = None
        current_direction_2 = None
        move_event_2 = None
        will_crash_2 = False
        crashed_tail_2 = False
        if self.game.two_players:
            pressed_direction_keys_queue_2 = deque(list())
            last_direction_2 = self.game.snake_2.directions[-1]
            current_direction_2 = last_direction_2
            speed_key = pg.K_RCTRL

        even_step = True        # switch each iteration of game-loop between True and False -> used for speed
        speed_count = 0
        speed_count_2 = 0
        running = True

        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

                    elif event.key == speed_key:
                        speed = True
                    elif event.key == pg.K_LEFT:
                        pressed_direction_keys_queue.append('l')
                    elif event.key == pg.K_RIGHT:
                        pressed_direction_keys_queue.append('r')
                    elif event.key == pg.K_UP:
                        pressed_direction_keys_queue.append('u')
                    elif event.key == pg.K_DOWN:
                        pressed_direction_keys_queue.append('d')

                    if self.game.two_players:
                        if event.key == pg.K_LCTRL:
                            speed_2 = True
                        elif event.key == pg.K_a:
                            pressed_direction_keys_queue_2.append('l')
                        elif event.key == pg.K_d:
                            pressed_direction_keys_queue_2.append('r')
                        elif event.key == pg.K_w:
                            pressed_direction_keys_queue_2.append('u')
                        elif event.key == pg.K_s:
                            pressed_direction_keys_queue_2.append('d')

                elif event.type == pg.KEYUP:
                    if event.key == speed_key:
                        speed = False
                    if self.game.two_players:
                        if event.key == pg.K_LCTRL:
                            speed_2 = False


            # update current direction for this step
            # if pressed_direction_keys_queue is empty, old value of current_direction is used (from last step)
            while pressed_direction_keys_queue:  # filter consecutive same directions like 'r', 'r', 'r'
                current_direction = pressed_direction_keys_queue.popleft()
                if current_direction != last_direction:
                    if not (even_step or speed):
                        pressed_direction_keys_queue.appendleft(current_direction)      # put back in if not even_step! (because didnt move!)
                    else:
                        last_direction = current_direction      # change last_direktion only if moved!
                    break

            # check if crash in this direction (no tail-ends!)
            current_direction, next_pos, will_crash = self.game.snake.prepare_move(current_direction)

            # Snake 2
            if self.game.two_players:


                # update current direction for this step
                # if pressed_direction_keys_queue is empty, old value of current_direction is used (from last step)
                while pressed_direction_keys_queue_2:  # filter consecutive same directions like 'r', 'r', 'r'
                    current_direction_2 = pressed_direction_keys_queue_2.popleft()
                    if current_direction_2 != last_direction_2:
                        if not (even_step or speed_2):
                            pressed_direction_keys_queue_2.appendleft(current_direction_2)      # put back in if not even_step! (because didnt move!)
                        else:
                            last_direction_2 = current_direction_2      # change last_direktion only if moved!
                        break

                # check if crash in this direction (no tail-ends!)
                current_direction_2, next_pos_2, will_crash_2 = self.game.snake_2.prepare_move(current_direction_2)

                # check if both snakes have same position in front of them
                if next_pos == next_pos_2:
                    will_crash = will_crash_2 = True

            # only move every second step, except if speed
            if even_step or speed:
                move_event = self.game.snake.move(current_direction)
            # move Snake 2
            if self.game.two_players:
                if even_step or speed_2:
                    move_event_2 = self.game.snake_2.move(current_direction_2)

            # check for crashed tail-end
            crashed_tail = self.game.snake.check_if_crashed_tail_end()
            if self.game.two_players:
                crashed_tail_2 = self.game.snake_2.check_if_crashed_tail_end()

            # combine both
            will_crash = will_crash or crashed_tail
            will_crash_2 = will_crash_2 or crashed_tail_2

            # proceed only if not crashed
            if not (will_crash or will_crash_2):

                self.draw_map()
                self.draw_sweet()
                self.draw_snake(self.game.snake)
                if self.game.two_players:
                    self.draw_snake(self.game.snake_2)

                if not self.game.two_players:
                    if move_event == "EATEN":
                        play_sound(sa.eat_sound)
                        highscore_changed = self.game.inc_score()
                        if highscore_changed:
                            play_sound(sa.beat_highscore_sound)
                        self.game.spawn_sweet()
                else:
                    if move_event == "EATEN":
                        play_sound(sa.eat_sound)
                        self.game.score_good += 1
                        self.draw_two_player_score()
                        if self.game.score_good == self.game.max_score:
                            return "GOOD"
                        self.game.spawn_sweet()
                    elif move_event_2 == "EATEN":
                        play_sound(sa.eat_sound_2)
                        self.game.score_evil += 1
                        self.draw_two_player_score()
                        if self.game.score_evil == self.game.max_score:
                            return "EVIL"
                        self.game.spawn_sweet()

                if move_event == "PORTAL":
                    play_sound(sa.portal_sound)
                if move_event_2 == "PORTAL":
                    play_sound(sa.portal_sound_2)

                if not self.game.two_players:
                    self.draw_score()
                else:
                    self.draw_two_player_score()
                pg.display.flip()

            # if crash ahead
            else:
                if not self.game.two_players:
                    play_sound(sa.damage_sound)
                    return ""
                else:
                    if will_crash and will_crash_2:
                        play_sound(sa.damage_sound)
                        play_sound(sa.damage_sound_2)
                        return "DRAW"
                    elif will_crash:
                        play_sound(sa.damage_sound)
                        return "EVIL"
                    elif will_crash_2:
                        play_sound(sa.damage_sound_2)
                        return "GOOD"

            if speed:
                if speed_count % 10 == 0:
                    play_sound(sa.boost_sound)
                speed_count += 1
            else:
                speed_count = 0

            if speed_2:
                if speed_count_2 % 10 == 0:
                    play_sound(sa.boost_sound_2)
                speed_count_2 += 1
            else:
                speed_count_2 = 0

            move_event = ""
            move_event_2 = ""
            even_step = not even_step

            if self.inc_speed:
                current_speed = self.start_speed + self.game.score // 2
            else:
                current_speed = self.start_speed
            self.clock.tick(current_speed * 2)  # limits FPS to 60



