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


class Bullet(Monster):
    speed: int = 10
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
    score: int = 0
    ready: bool = False
    connection = None

    had_action: bool = False
    
    def __init__(self, player_id):
        if player_id == 0:
            super().__init__(128, 320)
        elif player_id == 1:
            super().__init__(512 - 128, 320)
        else:
            raise ValueError('player_id')
        self.player_id = player_id

    def set(self, connection):
        self.connection = connection
        self.ready = True

    def set_had_action(self):
        self.had_action = True

    def get_serialized_data(self):
        data = super().get_serialized_data()
        data['player_id'] = self.player_id
        return data


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
            return

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
