from battle_city.monsters import Monster


class Tank(Monster):
    is_shot: bool = False
    SIZE = 32

    def set_speed(self, speed: int):
        self.speed = min(max(speed, 0), 2)

    def set_shot(self):
        self.is_shot = True

    def set_direction(self, direction):
        super().set_direction(direction)

        # round after change direction like in original battle city.
        # with rounding is more easy to move tank beetwen walls
        part_size = self.SIZE / 2
        if direction in {Direction.UP, Direction.DOWN}:
            self.position.x = round(self.position.x / part_size) * part_size
        else:
            self.position.y = round(self.position.y / part_size) * part_size
