from enum import Enum


class Vec(object):
    __slots__ = ('x', 'y')
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
