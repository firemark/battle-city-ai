from battle_city.monsters.tank import Tank
from battle_city.basic import Direction


def make_tank(x=128, y=128, direction=None):
    tank = Tank(x, y)
    if direction:
        tank.direction = direction
    return tank


def test_speed_max():
    tank = make_tank()
    tank.set_speed(5)

    assert tank.speed == 2


def test_speed_min():
    tank = make_tank()
    tank.set_speed(-1)

    assert tank.speed == 0


def test_snap_to_grid_after_direction_up():
    tank = make_tank(x=24, y=24, direction=Direction.LEFT)  # grid tile is 16x16
    tank.set_direction(Direction.UP)

    assert tank.position.x == 32
    assert tank.position.y == 24


def test_snap_to_grid_after_direction_down():
    tank = make_tank(x=24, y=24, direction=Direction.LEFT)  # grid tile is 16x16
    tank.set_direction(Direction.DOWN)

    assert tank.position.x == 32
    assert tank.position.y == 24


def test_snap_to_grid_after_direction_left():
    tank = make_tank(x=24, y=24)  # grid tile is 16x16
    tank.set_direction(Direction.LEFT)

    assert tank.position.x == 24
    assert tank.position.y == 32


def test_snap_to_grid_after_direction_right():
    tank = make_tank(x=24, y=24)  # grid tile is 16x16
    tank.set_direction(Direction.RIGHT)

    assert tank.position.x == 24
    assert tank.position.y == 32


def test_shot():
    tank = make_tank()
    tank.set_shot()

    assert tank.is_shot is True
