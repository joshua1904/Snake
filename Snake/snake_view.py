"""
The front-end with pygame
"""
from pathlib import Path

import snake_classes
import assets
import pygame

pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class GameView:
    """
    The view of a single game
    """
    def __init__(self, game: snake_classes.Game, cell_size=30):
        self.game = game
        self.cell_size = cell_size
        self.map_surface: pygame.Surface        # the (immutable) background with walls and portals

        self.background_image = assets.wall_image
        self._init_map_surface()

    def _init_map_surface(self):
        """Prepare the map_surface"""
        self.map_surface = SCREEN.copy()
        self.map_surface.fill("black")

        # Background with border
        border = pygame.Surface(((self.game.board.dim.x + 2) * self.cell_size,
                                 (self.game.board.dim.x + 2) * self.cell_size))
        border.fill("darkorchid4")
        self.draw_to_board(border, -1, -1, self.map_surface)
        background_surface = self._create_background(self.background_image,
                                                     (self.game.board.dim.x * self.cell_size,
                                                      self.game.board.dim.x * self.cell_size))
        self.draw_to_board(background_surface, 0, 0, self.map_surface)

        for wall in self.game.board.walls:
            self.draw_to_board(assets.wall_image, wall.x, wall.y, self.map_surface)
        draw_picture(portal_image, portal1[0], portal1[1], map_surface)
        draw_picture(portal_image, portal2[0], portal2[1], map_surface)

    def _create_background(self, image: pygame.image, tile_size=(360, 360), darker=90) -> pygame.Surface:
        """Generate Background-Imgae"""
        scaled_image = pygame.transform.smoothscale(image, tile_size)
        scaled_image.fill((darker, darker, darker), special_flags=pygame.BLEND_RGB_SUB)
        background_surface = pygame.Surface(map_size)
        for x in range(0, map_size[0] // tile_size[0] + 1):
            for y in range(0, map_size[1] // tile_size[1] + 1):
                background_surface.blit(scaled_image, (x * tile_size[0], y * tile_size[1]))
        return background_surface


def game_loop():

    while True:
        pygame.display.flip()
        CLOCK.tick(10)  # limits FPS to 60


if __name__ == "__main__":
    game_loop()

