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
                 game: sc.Game, cell_size=30, base_speed=10):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.clock = clock

        self.game = game
        self.cell_size = cell_size
        self.base_speed = base_speed

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

    def draw_snake(self):
        """
        Draw the snake
        end -> parts -> head
        """
        snake = self.game.snake
        head_pos = snake.positions[-1]
        head_dir = snake.directions[-1]
        end_pos = snake.positions[0]
        end_dir = snake.directions[1]

        # Draw head
        self.draw_to_board(sa.snake_head[head_dir], head_pos.x, head_pos.y, self.screen)

        # Draw tail
        self.draw_to_board(sa.snake_end[end_dir], end_pos.x, end_pos.y, self.screen)

        # Draw middle parts
        for i, part_pos in enumerate(snake.positions):
            if i in range(1, len(snake.positions) - 1):
                part_dir = snake.directions[i]
                part_next_dir = snake.directions[i + 1]
                corner_id = GameView.MIDDLE_PARTS[part_dir + part_next_dir]
                self.draw_to_board(sa.snake_part[corner_id], part_pos.x, part_pos.y, self.screen)

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

    def game_loop(self):
        """the main loop"""

        # allow only certain events (no mouse)
        pg.event.set_allowed((pg.QUIT, pg.KEYDOWN, pg.KEYUP))

        # save pressed keys in queue
        pressed_direction_keys_queue = deque(list())

        speed = False
        speed_count = 0
        last_direction = self.game.snake.directions[-1]     
        wanted_direction = last_direction
        running = True

        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_SPACE:
                        speed = True
                    elif event.key == pg.K_LEFT:
                        pressed_direction_keys_queue.append('l')
                    elif event.key == pg.K_RIGHT:
                        pressed_direction_keys_queue.append('r')
                    elif event.key == pg.K_UP:
                        pressed_direction_keys_queue.append('u')
                    elif event.key == pg.K_DOWN:
                        pressed_direction_keys_queue.append('d')

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        speed = False

            if not pressed_direction_keys_queue:
                last_direction = self.game.snake.directions[-1]         
                move_event = self.game.snake.move(last_direction)
            else:
                while pressed_direction_keys_queue:  # filter consecutive same directions like 'r', 'r', 'r'
                    wanted_direction = pressed_direction_keys_queue.popleft()
                    if wanted_direction != last_direction:
                        last_direction = wanted_direction
                        break
                move_event = self.game.snake.move(wanted_direction)

            if move_event != "CRASH":

                self.draw_map()
                self.draw_sweet()
                self.draw_snake()

                if move_event == "EATEN":
                    play_sound(sa.eat_sound)
                    highscore_changed = self.game.inc_score()
                    if highscore_changed:
                        play_sound(sa.beat_highscore_sound)
                    self.game.spawn_sweet()

                elif move_event == "PORTAL":
                    play_sound(sa.portal_sound)

                self.draw_score()
                pg.display.flip()

            else:
                play_sound(sa.damage_sound)
                return

            if speed:
                if speed_count % 10 == 0:
                    play_sound(sa.boost_sound)
                self.clock.tick(self.base_speed * 2)
                speed_count += 1
            else:
                self.clock.tick(self.base_speed)  # limits FPS to 60
                speed_count = 0


