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

