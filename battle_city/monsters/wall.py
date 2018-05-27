from battle_city.basic import Direction

from uuid import UUID, uuid4
from pygame import Rect


class Wall(object):
    id: UUID
    is_destroyed: bool
    position: Rect
    SIZE = 32
    PART_SIZE = 8

    def __init__(self, x: int, y: int):
        self.id = uuid4()
        size = self.SIZE
        self.position = Rect(x, y, size, size)
        self.is_destroyed = False

    def hurt(self, direction: Direction):
        position = self.position
        part = self.PART_SIZE
        if self.is_destroyed:
            return True

        if direction == Direction.UP:
            position.height -= part
        elif direction == Direction.DOWN:
            position.height -= part
            position.y += part
        elif direction == Direction.RIGHT:
            position.width -= part
            position.x += part
        elif direction == Direction.LEFT:
            position.width -= part

        if position.width == 0 or position.height == 0:
            self.is_destroyed = True

        return True


class Metal(Wall):

    def hurt(self, direction: Direction):
        return True


class Water(Wall):

    def hurt(self, direction: Direction):
        return False
