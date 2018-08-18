from battle_city.basic import Direction

from uuid import UUID, uuid4
from pygame import Rect


class Wall(object):
    id: UUID
    position: Rect
    SIZE = 32

    def __init__(self, x: int, y: int):
        self.id = uuid4()
        size = self.SIZE
        self.position = Rect(x, y, size, size)

    def hurt(self, direction: Direction) -> (bool, bool):
        """

        :param direction:
        :return: (is_destroyed, is_touched)
        """
        return True, True


class TinyWall(Wall):
    SIZE = 8


class Metal(Wall):

    def hurt(self, direction: Direction) -> (bool, bool):
        return False, True


class Water(Wall):

    def hurt(self, direction: Direction):
        return False, False
