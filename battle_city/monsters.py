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

    SIZE = 8 

    def __init__(self, x: int, y: int):
        self.id = uuid4()
        size = self.SIZE
        self.position = Rect(x, y, size, size)
        self.center = (size // 2, size // 2)

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
        return self.position.collidelistall(group)

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


class Bullet(Monster):
    speed: int = 5
    parent_type: str = None
    parent_id: UUID = None
    SIZE = 4

    def set_parent(self, parent: Monster):
        self.parent_type = parent.get_type()
        self.parent_id  = parent.id


class Tank(Monster):
    is_shot: bool = False
    SIZE = 32

    def set_speed(self, speed: int):
        self.speed = min(max(speed, 0), 2)

    def set_shot(self):
        self.is_shot = True


class NPC(Tank):
    direction: Direction = Direction.DOWN

    def do_something(self):
        pass


class Player(Tank):
    player_id: int
    ready: bool = False
    connection = None
    
    def __init__(self, player_id):
        if player_id == 0:
            super().__init__(64, 180)
        elif player_id == 1:
            super().__init__(512 - 64, 180)
        else:
            raise ValueError('player_id')
        self.player_id = player_id

    def set(self, connection):
        self.connection = connection
        self.ready = True

    def get_serialized_data(self):
        data = super().get_serialized_data()
        data['player_id'] = self.player_id
        return data
