from pygame.rect import Rect

from battle_city.monsters import Monster
from battle_city.basic import Direction


class Bullet(Monster):
    speed = 8
    SIZE = 4

    def get_long_collision_rect(self):
        pos = self.position
        x = pos.x
        y = pos.y
        size = self.SIZE
        half_size = size // 2

        if self.direction in [Direction.UP, Direction.DOWN]:
            return Rect(x + half_size - 16, y, 32, size)
        else:
            return Rect(x, y + half_size - 16, size, 32)
