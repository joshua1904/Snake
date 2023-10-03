"""
The back-end game logic
"""
from __future__ import annotations

import random
from collections import namedtuple, deque
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, List, Any, Deque

# Subclass of Tuple with named parameters .x and .y
XYTuple = namedtuple('XYTuple', ['x', 'y'])


@dataclass(frozen=True)                         # frozen=True -> immutable
class BoardPosition:
    """
    The position of a field in the game-board
    Has reference to GameBoard-class to adapt position to board size
    """
    x: int
    y: int
    board: GameBoard = field(repr=False, compare=False)     # repr=False: don't print board in string, compare=False: don't use board for ==

    def __post_init__(self):
        """Adapt position to board size ("no borders")"""
        super().__setattr__('x', self.x % self.board.dim.x)
        super().__setattr__('y', self.y % self.board.dim.y)

    def __add__(self, other):
        """
        BoardPosition(3, 2) + BoardPosition(1, 1) = BoardPosition(4, 3)
        Works also for XYTuple and tuple as second argument
        """
        if isinstance(other, (BoardPosition, XYTuple)):
            new_x, new_y = self.x + other.x, self.y + other.y
        elif isinstance(other, tuple) and len(other) == 2:
            new_x, new_y = self.x + other[0], self.y + other[1]
        else:
            raise(TypeError('Can only add BoardPosition, XYTuple oder tuple (len==2) to BoardPosition.'))
        return BoardPosition(new_x, new_y, self.board)

    def __sub__(self, other):
        """
        BoardPosition(3, 2) - BoardPosition(1, 1) = BoardPosition(2, 1)
        Works also for XYTuple and tuple as second argument
        """
        if isinstance(other, (BoardPosition, XYTuple)):
            new_x, new_y = self.x - other.x, self.y - other.y
        elif isinstance(other, tuple) and len(other) == 2:
            new_x, new_y = self.x - other[0], self.y - other[1]
        else:
            raise (TypeError('Can only subtract BoardPosition, XYTuple oder tuple (len==2) from BoardPosition.'))
        return BoardPosition(new_x, new_y, self.board)


@dataclass
class BoardCell:
    """
    A Cell on the Game-Board
    """
    pos: BoardPosition
    type: str
    subtype: int
    partner: BoardCell = None            # only for Portals


class Snake:
    """
    The snake
    """
    DIRECTIONS = {'l': (-1, 0), 'r': (1, 0), 'u': (0, -1), 'd': (0, 1)}

    def __init__(self, board: GameBoard, start_pos: BoardPosition, start_direction: str):
        """
        Saves the snake in two double-ended-lists (deque), one for the positions and one for the directions
        """
        self.board: GameBoard = board
        self.positions: Deque[BoardPosition] = deque([start_pos])
        self.directions: Deque[str] = deque([start_direction])

    def _save_direction(self, new_direction: str):
        """
        Save the new direction to self.directions
        :param new_direction: the direction to move from the current head position
        """
        last_direction = self.directions[-1]
        if last_direction != new_direction:
            self.directions.append(f"{last_direction}{new_direction}")
        else:
            self.directions.append(new_direction)

    def move(self, direction: str) -> bool:
        """
        Saves a new snake-part to the snake in front (the head)
        and removes the last part (the tail)
        """
        last_position = self.positions[-1]
        new_position = last_position + Snake.DIRECTIONS[direction]

        # Check for crash
        if new_position in self.positions or new_position in self.board.walls:
            return False

        # Check for portals
        elif new_position in self.board.portals:
            # play_sound(portal_sound)
            start_portal = self.board.portals[new_position]
            target_portal = start_portal.partner
            new_position = target_portal.pos + Snake.DIRECTIONS[direction]

        # Append new head
        self.positions.append(new_position)
        self._save_direction(direction)

        # Check for sweet -> only pop tail if not eaten
        if new_position != self.board.sweet.pos:
            self.positions.popleft()
            self.directions.popleft()

        return True


class GameBoard:
    """
    The current game-board
    """

    def __init__(self, map_list: List[List[Any]]):
        """"""
        dim_x, dim_y = len(map_list[0]), len(map_list)
        self.dim = XYTuple(dim_x, dim_y)
        self.walls: Dict[BoardPosition, BoardCell] = {}
        self.portals: Dict[BoardPosition, BoardCell] = {}
        self.sweet: BoardCell

        self._load_map_from_list(map_list)
        self.sweet = self.spawn_sweet()

    def _load_map_from_list(self, map_list: List[List[Any]]):
        """
        Load BoardCells to self.walls and self.portals from map_list
        WALLS have id in range 1...3
        PORTALS have id >= 4, there have to be exactly two with the same id in map_list
        """
        assert self.dim.x == len(map_list[0]) and self.dim.y == len(map_list), "Map-dimension doesn't match map_str"

        portals_temp_dict: Dict[int, Optional[BoardCell]] = {}        # to find partner-portals

        for row_counter, row in enumerate(map_list):
            for col_counter, col in enumerate(row):

                if col.isdigit():           # ignore non-digit cells (e.g. snake)
                    cell_id = int(col)

                    # Walls
                    if cell_id in range(1, 4):
                        pos = BoardPosition(col_counter, row_counter, self)
                        cell = BoardCell(pos, "WALL", cell_id)
                        self.walls[pos] = cell

                    # Portals
                    elif cell_id >= 4:
                        pos = BoardPosition(col_counter, row_counter, self)
                        cell = BoardCell(pos, "PORTAL", cell_id - 3)
                        self.portals[pos] = cell
                        if cell_id in portals_temp_dict:                # other one was found already
                            if portals_temp_dict[cell_id]:                  # check that only one was found (in case there are more than two with the same cell_id)
                                cell.partner = portals_temp_dict[cell_id]       # cross-link portals
                                cell.partner.partner = cell                     # cross-link portals
                                portals_temp_dict[cell_id] = None               # remember that both were found
                            else:
                                raise Exception(f"More than two portals with the same id ({cell_id}) found in map_list")
                        else:                                           # it's the first one
                            portals_temp_dict[cell_id] = cell

        # check that all portals have a partner
        assert all(v is None for v in portals_temp_dict.values()), (f"There are portals with no partner in "
                                                                    f"map_list: {map_list}")

    def spawn_sweet(self):
        """
        Spawn a sweet, not in walls, not in portals and not in TODO: snake positions
        """
        sweet_x = random.randint(0, self.dim.x)
        sweet_y = random.randint(0, self.dim.y)
        sweet_pos = BoardPosition(sweet_x, sweet_y, self)
        if sweet_pos not in self.walls and sweet_pos not in self.portals:
            sweet_cell = BoardCell(sweet_pos, "SWEET", 1)
            return sweet_cell
        else:
            return self.spawn_sweet()


class Game:
    """The game"""

    def __init__(self, map_list: List[List[Any]]):
        self.board = GameBoard(map_list)
        self.snake: Snake

        self._init_snake(map_list)

    def _init_snake(self, map_list: List[List[Any]]):
        for row_counter, row in enumerate(map_list):
            for col_counter, cell_id in enumerate(row):
                if cell_id in ('l', 'r', 'u', 'd'):
                    pos = BoardPosition(col_counter, row_counter, self.board)
                    self.snake = Snake(self.board, pos, cell_id)



