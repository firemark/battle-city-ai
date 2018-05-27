from battle_city.basic import Direction
from battle_city.monsters.tank import Tank

from random import random, randint, choice


class NPC(Tank):
    direction: Direction = Direction.DOWN
    speed: int = 2

    def do_something(self) -> bool:
        if random() > 0.4:
            return False

        action = randint(1, 2)
        if action == 1:
            directions = [
                Direction.UP, Direction.DOWN,
                Direction.LEFT, Direction.RIGHT,
            ]
            direction = choice(directions)
            self.set_direction(direction)
        else:
            self.set_shot()

        return True
