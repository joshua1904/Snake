"""
All classes for the game logic
"""
from collections import namedtuple
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple, List, Dict, Self, Optional

import pygame

# Subclass of Tuple with named parameters .x and .y
XYTuple = namedtuple('XYTuple', ['x', 'y'])


class GameBoard:
    """
    The current game-board
    """

    def __init__(self, dim_x: int, dim_y: int, map_list: list):
        """
        (dim_x, dim_y) is the dimension of the board
        """
        self.dim = XYTuple(dim_x, dim_y)
        self.walls: Dict[BoardPosition, BoardCell] = {}
        self.portals: Dict[BoardPosition, BoardCell] = {}
        self.load_map_from_list(map_list)

    def load_map_from_list(self, map_list: list):
        """
        Load BoardCells to self.walls and self.portals from map_list
        WALLS have id in range 1...3
        PORTALS have id >= 4, there have to be exactly two with the same id in map_list
        """
        assert self.dim.x == len(map_list[0]) and self.dim.y == len(map_list), "Map-dimension doesn't match map_str"

        portals_temp_dict: Dict[int, Optional[BoardCell]] = {}        # to find partner-portals

        for row_counter, row in enumerate(map_list):
            for col_counter, col in enumerate(row):
                pos = BoardPosition(col_counter, row_counter, self)

                try:
                    cell_id = int(col)
                except ValueError:
                    raise ValueError(f"map_str value ({col}) can't be converted to int")

                # Walls
                if cell_id in range(1, 4):
                    cell = BoardCell(pos, "WALL", cell_id)
                    self.walls[pos] = cell

                # Portals
                elif cell_id >= 4:
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


@dataclass(order=True, frozen=True)                         # order=True generates <,<=, >=,> methods, frozen=True -> immutable
class BoardPosition:
    """
    The position of a field in the game-board
    Has reference to GameBoard-class to adapt position to board size
    """
    x: int
    y: int
    board: GameBoard = field(repr=False, compare=False)     # repr=False: don't print board in string, compare=False: don't use board for <,>, <=, =>

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
    partner: Self = None            # only for Portals, type Self is BoardCell



