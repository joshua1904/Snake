"""
The front-end with pygame
"""
import itertools
from collections import deque
from pathlib import Path

import snake_classes
import assets
import pygame

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()


def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()


class GameView:
    """
    The view of a single game
    """
    MIDDLE_PARTS = {
        'l': 'rl', 'r': 'rl',
        'u': 'ud', 'd': 'ud',
        'rd': 'dr', 'ul': 'dr',
        'dr': 'ul', 'lu': 'ul',
        'ru': 'ur', 'dl': 'ur',
        'ur': 'dl', 'ld': 'dl'
    }

    def __init__(self, game: snake_classes.Game, cell_size=30):
        self.game = game
        self.cell_size = cell_size
        self.map_width_px = self.game.board.dim.x * self.cell_size
        self.map_height_px = self.game.board.dim.y * self.cell_size
        self.map_surface: pygame.Surface        # the (immutable) background with walls and portals

        self.background_image = assets.wall_image
        self._init_map_surface()

    def _init_map_surface(self):
        """Prepare the map_surface"""
        self.map_surface = SCREEN.copy()
        self.map_surface.fill("black")

        # Background with border
        border = pygame.Surface((self.map_width_px + (2 * self.cell_size),
                                 self.map_height_px + (2 * self.cell_size)))
        border.fill("darkorchid4")
        self.draw_to_board(border, -1, -1, self.map_surface)
        background_surface = self._create_background(self.background_image,
                                                     (self.map_width_px,
                                                      self.map_height_px))
        self.draw_to_board(background_surface, 0, 0, self.map_surface)

        # Walls
        for wall in self.game.board.walls:
            self.draw_to_board(assets.wall_image, wall.x, wall.y, self.map_surface)

        # Portals
        for portal in self.game.board.portals:
            self.draw_to_board(assets.portal_image, portal.x, portal.y, self.map_surface)

    def _create_background(self, image: pygame.image, tile_size=(360, 360), darker=90) -> pygame.Surface:
        """
        Generate Background-Imgae
        :param image: the image to use for the background
        :param tile_size: how big the image should be scaled in pixels
        :param darker: r, g, b values to be subtracted from image (0-255)
        :return: the background surface (as big as the map)
        """
        scaled_image = pygame.transform.smoothscale(image, tile_size)
        scaled_image.fill((darker, darker, darker), special_flags=pygame.BLEND_RGB_SUB)
        background_surface = pygame.Surface((self.map_width_px, self.map_height_px))
        for x in range(0, self.map_width_px // tile_size[0] + 1):
            for y in range(0, self.map_height_px // tile_size[1] + 1):
                background_surface.blit(scaled_image, (x * tile_size[0], y * tile_size[1]))
        return background_surface

    def draw_to_board(self, image: pygame.image, x: int, y: int, surface: pygame.Surface):
        """
        :param image: the image to draw
        :param x: x-Coord. on the board (in cells)
        :param y: y-Coord. on the board (in cells)
        :param surface: the surface to draw to
        """
        surface.blit(image, (x * self.cell_size + SCREEN_WIDTH // 2 - self.map_width_px // 2,
                             y * self.cell_size + SCREEN_HEIGHT // 2 - self.map_height_px // 2))

    def draw_snake(self):
        """
        Draw the snake
        end -> parts -> head
        """
        snake = self.game.snake
        head_pos = snake.positions[-1]
        head_dir = snake.directions[-1][-1]                         # only last direction: 'ru' -> 'u'
        end_pos = snake.positions[0]
        end_dir = snake.directions[0][-1]                           # only last direction: 'ru' -> 'u'
        middle_pos = itertools.islice(snake.positions, 1, len(snake.positions) - 1)
        middle_dir = itertools.islice(snake.directions, 1, len(snake.positions) - 1)

        # Draw head
        self.draw_to_board(assets.snake_head[head_dir], head_pos.x, head_pos.y, SCREEN)

        # Draw tail
        self.draw_to_board(assets.snake_end[end_dir], end_pos.x, end_pos.y, SCREEN)

        # Draw middle parts
        for part_pos, part_dir in zip(middle_pos, middle_dir):
            self.draw_to_board(assets.snake_part[GameView.MIDDLE_PARTS[part_dir]], part_pos.x, part_pos.y, SCREEN)

    def draw_map(self):
        """Draw the background and map to the screen"""
        SCREEN.blit(self.map_surface, (0, 0))

    def draw_sweet(self):
        """Draw the sweet on the screen"""
        sweet = self.game.sweet
        self.draw_to_board(assets.sweet_image, sweet.pos.x, sweet.pos.y, SCREEN)

    def game_loop(self):
        """the main loop"""

        # allow only certain events (no mouse)
        pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP))

        # save pressed keys in queue
        pressed_direction_keys_queue = deque(list())

        speed = False
        speed_count = 0
        last_direction = self.game.snake.directions[-1][-1]     # only last direction: 'ru' -> 'u'
        wanted_direction = last_direction
        running = True

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        speed = True
                    elif event.key == pygame.K_LEFT:
                        pressed_direction_keys_queue.append('l')
                    elif event.key == pygame.K_RIGHT:
                        pressed_direction_keys_queue.append('r')
                    elif event.key == pygame.K_UP:
                        pressed_direction_keys_queue.append('u')
                    elif event.key == pygame.K_DOWN:
                        pressed_direction_keys_queue.append('d')

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        speed = False

            if not pressed_direction_keys_queue:
                last_direction = self.game.snake.directions[-1][-1]         # only last direction: 'ru' -> 'u'
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
                    play_sound(assets.eat_sound)
                    self.game.score += 1
                    self.game.spawn_sweet()

                pygame.display.flip()

            else:
                play_sound(assets.damage_sound)
                return

            if speed:
                if speed_count % 10 == 0:
                    play_sound(assets.boost_sound)
                CLOCK.tick(10)
                speed_count += 1
            else:
                CLOCK.tick(5)  # limits FPS to 60
                speed_count = 0


if __name__ == "__main__":

    map_list = [[1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 'r', 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1]]

    game = snake_classes.Game(map_list)

    game_view = GameView(game)

    game_view.game_loop()

