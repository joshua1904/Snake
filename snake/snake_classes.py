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

    def __repr__(self):
        return f"BP({self.x}, {self.y})"


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
    DIRECTIONS = {'l': (-1, 0), 'u': (0, -1), 'r': (1, 0), 'd': (0, 1)}
    OPPOSITES = ['l', 'u', 'r', 'd']            # OPPOSITES[i-2] is opposite direction of OPPOSITES[i]

    def __init__(self, game: Game, start_pos: BoardPosition, start_direction: str):
        """
        Saves the snake in two double-ended-lists (deque), one for the positions and one for the directions
        """
        self.game = game
        self.positions: Deque[BoardPosition] = deque([start_pos - Snake.DIRECTIONS[start_direction], start_pos])
        self.directions: Deque[str] = deque([start_direction, start_direction])

    def move(self, direction: str) -> str:
        """
        Saves a new snake-part to the snake in front (the head)
        and removes the last part (the tail)
        """
        move_event = ""

        # do not move in opposite direction
        last_direction = self.directions[-1]
        i = Snake.OPPOSITES.index(last_direction)
        if direction == Snake.OPPOSITES[i - 2]:
            direction = last_direction

        last_position = self.positions[-1]
        new_position = last_position + Snake.DIRECTIONS[direction]

        # Check for crash
        if new_position in self.positions or new_position in self.game.board.walls:
            return "CRASH"

        # Check for portals
        elif new_position in self.game.board.portals:
            start_portal = self.game.board.portals[new_position]
            target_portal = start_portal.partner
            new_position = target_portal.pos + Snake.DIRECTIONS[direction]
            move_event = "PORTAL"

        # Append new head
        self.positions.append(new_position)
        self.directions.append(direction)

        # Check for sweet -> only pop tail if not eaten
        if new_position == self.game.sweet.pos:
            return "EATEN"

        self.positions.popleft()
        self.directions.popleft()
        # print(self.directions)
        # print(self.positions)

        return move_event


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

    def _load_map_from_list(self, map_list: List[List[Any]]):
        """
        Load BoardCells to self.walls and self.portals from map_list
        WALLS have id in range 1...3
        PORTALS have id >= 4, there have to be exactly two with the same id in map_list
        """
        # print(map_list)
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
        # print(self.dim)
        # print(self.walls)
        # print(self.portals)


class Game:
    """The game"""

    def __init__(self, map_list: List[List[Any]], highscore: int):

        self.board = GameBoard(map_list)
        self.snake: Snake
        self.sweet: BoardCell

        self.score = 0
        self.highscore = highscore
        self.highscore_changed = False

        found_snake = self._init_snake(map_list)
        if not found_snake:
            raise Exception("No snake starting-position ('l', 'r', 'u', 'd') in map_list!")
        self.spawn_sweet()

    def _init_snake(self, map_list: List[List[Any]]) -> bool:
        for row_counter, row in enumerate(map_list):
            for col_counter, cell_id in enumerate(row):
                if cell_id in ('l', 'r', 'u', 'd'):
                    pos = BoardPosition(col_counter, row_counter, self.board)
                    self.snake = Snake(self, pos, cell_id)
                    return True
        return False

    def spawn_sweet(self):
        """
        Spawn a sweet, not in walls, not in portals and not in snake positions
        """
        sweet_x = random.randint(0, self.board.dim.x)
        sweet_y = random.randint(0, self.board.dim.y)
        sweet_pos = BoardPosition(sweet_x, sweet_y, self.board)

        if (sweet_pos not in self.board.walls.keys()
                and sweet_pos not in self.board.portals.keys()
                and sweet_pos not in self.snake.positions):

            self.sweet = BoardCell(sweet_pos, "SWEET", 1)
            return None
        else:
            return self.spawn_sweet()       # recursive

    def inc_score(self) -> bool:
        """
        Increase the score by 1 and check if highscore is met
        """
        self.score += 1
        if self.score > self.highscore:
            self.highscore = self.score
            self.highscore_changed = True
        return self.highscore_changed





