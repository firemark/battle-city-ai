from pygame.rect import Rect
from uuid import uuid4


class Coin:
    SIZE = 32
    id = None  # type: UUID
    position = None

    def __init__(self, x, y):
        self.id = uuid4()
        self.position = Rect(x, y, self.SIZE, self.SIZE)

    def get_type(self):
        return self.__class__.__name__.lower()

    def get_position(self):
        return dict(
            x=self.position.x,
            y=self.position.y,
        )

    def __repr__(self):
        pos = self.position
        return 'Coin<{}, {}>'.format(pos.x, pos.y)