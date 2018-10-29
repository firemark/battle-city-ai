from battle_city.monsters import Monster
from battle_city.basic import Direction

from pygame import Rect


class Tank(Monster):
    HOR_DIRECTIONS = {Direction.LEFT, Direction.RIGHT}
    VER_DIRECTIONS = {Direction.UP, Direction.DOWN}
    is_shot = False
    SIZE = 32

    def set_speed(self, speed: int):
        self.speed = min(max(speed, 0), 2)

    def set_shot(self):
        self.is_shot = True

    def set_direction(self, direction):
        old_direction = self.direction
        super().set_direction(direction)

        # round after change direction like in original battle city.
        # with rounding is more easy to move tank beetwen walls
        part_size = self.SIZE / 2
        if direction in self.VER_DIRECTIONS and old_direction not in self.VER_DIRECTIONS:
            self.position.x = round(self.position.x / part_size) * part_size
            return

        if direction in self.HOR_DIRECTIONS and old_direction not in self.HOR_DIRECTIONS:
            self.position.y = round(self.position.y / part_size) * part_size

    def get_grid_position(self):
        position = self.position

        # (x >> 4) << 4 is faster than floor(x / 16) * 16
        x = (position.x >> 4) << 4
        y = (position.y >> 4) << 4

        return Rect(
            x,
            y,
            (((position.right + 15) >> 4) << 4) - x,
            (((position.bottom + 15) >> 4) << 4) - y,
        )
