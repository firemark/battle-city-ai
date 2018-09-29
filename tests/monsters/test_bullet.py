from battle_city.monsters import Bullet
from battle_city.basic import Direction

import pytest


@pytest.mark.parametrize('direction,x,y,w,h', [
    (Direction.UP, 0, 8, 32, 4),
    (Direction.DOWN, 0, 8, 32, 4),
    (Direction.LEFT, 8, 0, 4, 32),
    (Direction.RIGHT, 8, 0, 4, 32),
])
def test_get_long_collision(direction, x, y, w, h):
    bullet = Bullet(8, 8, direction=direction)
    rect = bullet.get_long_collision_rect()

    assert rect.x == x
    assert rect.y == y
    assert rect.width == w
    assert rect.height == h


@pytest.mark.parametrize('direction,offset,x,y', [
    (Direction.UP, 5, 0, 8 + 5),
    (Direction.UP, 10, 0, 8 + 10),
    (Direction.DOWN, 5, 0, 8 - 5),
    (Direction.LEFT, 5, 8 + 5, 0),
    (Direction.RIGHT, 5, 8 - 5, 0),
])
def test_get_log_collision_offset(direction, offset,x, y):
    bullet = Bullet(8, 8, direction=direction)
    rect = bullet.get_long_collision_rect(offset=offset)

    assert rect.x == x
    assert rect.y == y
