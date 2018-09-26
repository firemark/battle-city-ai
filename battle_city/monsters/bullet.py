from pygame.rect import Rect
from math import floor, ceil

from battle_city.monsters import Monster
from battle_city.basic import Direction


class Bullet(Monster):
    speed = 8
    SIZE = 4

    def get_long_collision_rect(self):
        pos = self.position
        size = self.SIZE
        half_size = size // 2

        if self.direction in [Direction.UP, Direction.DOWN]:
            x = floor((pos.x - half_size) / 16) * 16
            y = pos.y
            return Rect(x, y, 32, size)
        else:
            x = pos.x
            y = floor((pos.y - half_size) / 16) * 16
            return Rect(x, y, size, 32)
