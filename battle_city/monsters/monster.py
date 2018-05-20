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

    def set_direction(self, direction: Direction):
        self.direction = direction

    def get_type(self):
        return self.__class__.__name__.lower()

    def check_collision(self, group: List):
        rect_group = [monster.position for monster in group]
        indices = self.position.collidelistall(rect_group)
        return [group[index] for index in indices]

    def get_serialized_data(self):
        return dict(
            id=self.id.hex,
            type=self.get_type(),
            speed=self.speed,
            position=dict(x=self.position.x, y=self.position.y),
            is_freeze=self.is_freeze,
            direction=self.direction.value,
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
