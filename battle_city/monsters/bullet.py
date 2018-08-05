from battle_city.monsters import Monster

from uuid import UUID


class Bullet(Monster):
    speed: int = 10
    parent_type: str = None
    parent_id: UUID = None
    parent: Monster
    SIZE = 4

    def set_parent(self, parent: Monster):
        self.parent_type = parent.get_type()
        self.parent_id  = parent.id
        self.parent = parent
