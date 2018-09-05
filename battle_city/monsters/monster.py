from battle_city.basic import Direction

from uuid import UUID, uuid4
from pygame import Rect
from typing import List


class Monster(object):
    id: UUID
    direction: Direction = Direction.UP
    speed: int = 0
    is_freeze: bool = False
    position: Rect
    old_position: Rect

    SIZE = 8 

    def __init__(self, x: int, y: int):
        self.id = uuid4()
        size = self.SIZE
        self.position = Rect(x, y, size, size)
        self.set_old_position()

    def set_old_position(self):
        self.old_position = self.position.copy()

    def set_position(self, x: int, y: int):
        self.position.x = x
        self.position.y = y

    def set_speed(self, speed: int):
        self.speed = speed

    def set_freeze(self):
        self.is_freeze = True

    def unset_freeze(self):
        self.is_freeze = False

    def set_direction(self, direction: Direction):
        self.direction = direction

    def get_type(self):
        return self.__class__.__name__.lower()

    def check_collision_with_group(self, group: List, rect=None):
        rect_group = [monster.position for monster in group]
        rect = rect or self.position
        indices = rect.collidelistall(rect_group)
        return [group[index] for index in indices]

    def check_collision_with_old_position(self, monster):
        return self.old_position.colliderect(monster.position)

    def get_position(self):
        return dict(
            x=self.position.x,
            y=self.position.y,
        )

    def move(self):
        if self.is_freeze:
            return
        self.move_with_speed(self.speed)

    def move_with_speed(self, speed):
        position = self.position
        direction = self.direction

        if direction is Direction.UP:
            position.y -= speed
        elif direction is Direction.DOWN:
            position.y += speed
        elif direction is Direction.LEFT:
            position.x -= speed
        elif direction is Direction.RIGHT:
            position.x += speed
