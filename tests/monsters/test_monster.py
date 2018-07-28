from battle_city.monsters.monster import Monster
from battle_city.basic import Direction

import pytest

def make_monster(x=128, y=128):
    return Monster(x, y)


def test_set_position():
    monster = make_monster()
    monster.set_position(32, 32)

    assert monster.position.x == 32
    assert monster.position.y == 32


def test_set_old_position():
    monster = make_monster()
    monster.set_position(32, 32)
    monster.set_old_position()

    assert monster.old_position.x == 32
    assert monster.old_position.y == 32


def test_set_speed():
    monster = make_monster()
    monster.set_speed(10)
    assert monster.speed == 10


def test_set_direction():
    monster = make_monster()
    monster.set_direction(Direction.UP)

    assert monster.direction == Direction.UP


def test_get_type():
    monster = make_monster()

    assert monster.get_type() == 'monster'


@pytest.mark.parametrize('direction, dx, dy', [
    (Direction.UP, 0, -10),
    (Direction.DOWN, 0, 10),
    (Direction.LEFT, -10, 0),
    (Direction.RIGHT, 10, 0),
])
def test_move_with_speed_up(direction, dx, dy):
    monster = make_monster(x=128, y=128)
    monster.set_direction(direction)
    monster.move_with_speed(10)

    assert monster.position.x == 128 + dx
    assert monster.position.y == 128 + dy


def move_if_is_freeze():
    monster = make_monster(x=128, y=128)
    monster.set_direction(Direction.UP)
    monster.set_freeze()
    monster.move()

    assert monster.position.x == 128
    assert monster.position.y == 128


def move_if_is_not_freeze():
    monster = make_monster(x=128, y=128)
    monster.set_speed(10)
    monster.set_direction(Direction.UP)
    monster.move()

    assert monster.position.x == 128
    assert monster.position.y == 118
