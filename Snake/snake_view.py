"""
The front-end with pygame
"""
from pathlib import Path

import snake_classes
import assets
import pygame

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()


class GameView:
    """
    The view of a single game
    """
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

    def game_loop(self):
        """the main loop"""

        SCREEN.blit(self.map_surface, (0, 0))

        while True:
            pygame.display.flip()
            CLOCK.tick(10)  # limits FPS to 60


if __name__ == "__main__":

    map_list = [[1, 1, 1, 0, 0, 0, 0],
               [1, 0, 0, 0, 1, 1, 0],
               [1, 4, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 4, 0, 1],
               [0, 1, 1, 0, 0, 0, 1],
               [0, 0, 0, 0, 1, 1, 1]]

    board = snake_classes.GameBoard(map_list)

    game = snake_classes.Game(board)

    game_view = GameView(game)

    game_view.game_loop()

