from battle_city.basic import Direction
from battle_city.monsters.tank import Tank


class NPC(Tank):
    direction: Direction = Direction.DOWN
    speed: int = 2

    def do_something(self):
        pass
