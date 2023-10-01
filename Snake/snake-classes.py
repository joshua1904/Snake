"""
All classes for the game logic
"""
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Tuple

# Subclass of Tuple with named parameters .x and .y
XYTuple = namedtuple('XYTuple', ['x', 'y'])


class GameBoard:
    """
    The current game-board
    """

    def __init__(self, dim_x: int, dim_y: int):
        """
        (dim_x, dim_y) is the dimension of the board
        """
        self.dim = XYTuple(dim_x, dim_y)


@dataclass(order=True)                                      # order=True generates <,<=, >=,> methods
class BoardPosition:
    """The position of a field in the game-board"""
    x: int
    y: int
    board: GameBoard = field(repr=False, compare=False)     # repr=False: don't print board in string,
                                                            # compare=False: don't use board for <,>, <=, =>

    def __post_init__(self):
        """Adapt position to board size ("no borders")"""
        self.x = self.x % self.board.dim.x
        self.y = self.y % self.board.dim.y

    def __add__(self, other):
        if isinstan BoardPosition or other is XYTuple:
            self.x += other.x
            self.y += other.y
        elif other is Tuple

    def __sub__(self, other):
        return Point(self[0] - other[0], self[1] - other[1])