from pygame.rect import Rect
from math import floor

from battle_city.monsters import Monster
from battle_city.basic import Direction


class Bullet(Monster):
    speed = 8
    SIZE = 4

    def get_long_collision_rect(self, offset=0):
        pos = self.position
        size = self.SIZE
        half_size = size // 2

        if self.direction in [Direction.UP, Direction.DOWN]:
            x = floor((pos.x - half_size) / 16) * 16
            if self.direction is Direction.UP:
                y = pos.y + offset
            else:
                y = pos.y - offset
            return Rect(x, y, 32, size)
        else:
            if self.direction is Direction.LEFT:
                x = pos.x + offset
            else:
                x = pos.x - offset
            y = floor((pos.y - half_size) / 16) * 16
            return Rect(x, y, size, 32)
