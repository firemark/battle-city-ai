from battle_city.basic import Direction

from uuid import UUID, uuid4
from pygame import Rect

from battle_city.collections.sliced_array import SlicedArray


class Monster(object):
    id = None  # type: UUID
    direction = Direction.UP
    speed = 0
    is_freeze = False
    position = None  # type: Rect
    old_position = None  # type: Rect
    parent = None  # type: Monster

    SIZE = 8 

    def __init__(self, x: int, y: int, direction: Direction=None):
        self.id = uuid4()
        size = self.SIZE
        self.position = Rect(x, y, size, size)
        self.set_old_position()
        if direction:
            self.direction = direction

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

    def get_grid_position(self):
        position = self.position
        return Rect(
            # (x >> 4) << 4 is faster than floor(x / 16) * 16
            (position.x >> 4) << 4,
            (position.y >> 4) << 4,
            32,
            32,
        )

    def check_collision_with_group(self, group, rect=None, callback=None):
        callback = callback or (lambda m: m.position)
        rect = rect or self.position
        if isinstance(group, SlicedArray):
            group = group.find_nearest(rect)

        rect_group = list(map(callback, group))
        indices = rect.collidelistall(rect_group)
        return [group[index] for index in indices]

    def check_collision_with_old_position(self, monster):
        return self.old_position.colliderect(monster.position)

    def union_new_position_with_old(self):
        return self.position.union(self.old_position)

    def set_parent(self, parent):
        self.parent = parent

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
