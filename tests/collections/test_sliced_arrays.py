from pygame.rect import Rect

from battle_city.collections.sliced_array import SlicedArray
from battle_city.monsters import Coin

import pytest


def test_init_empty():
    array = SlicedArray(grid=32)
    assert array._parts == {}
    assert array._grid == 32
    assert len(array) == 0


def test_init_filled():
    coin_a = Coin(0, 0)
    coin_b = Coin(0, 0)
    array = SlicedArray([coin_a, coin_b], grid=16)

    assert array._parts == {
        (0, 0): [coin_a, coin_b],
    }
    assert len(array) == 2


def test_append():
    coin_a = Coin(0, 0)
    coin_b = Coin(16, 16)

    array = SlicedArray([coin_a], grid=16)
    array.append(coin_b)

    assert array._parts == {
        (0, 0): [coin_a],
        (1, 1): [coin_b],
    }
    assert len(array) == 2


def test_remove():
    coin_a = Coin(0, 0)
    coin_b = Coin(16, 16)
    array = SlicedArray([coin_a, coin_b], grid=16)
    array.remove(coin_b)

    assert array._parts == {
        (0, 0): [coin_a],
        (1, 1): [],
    }
    assert len(array) == 1


def test_remove_not_exists():
    coin_a = Coin(0, 0)
    coin_b = Coin(16, 16)
    array = SlicedArray([coin_a], grid=16)

    with pytest.raises(ValueError):
        array.remove(coin_b)

    assert array._parts == {
        (0, 0): [coin_a],
        (1, 1): [],
    }
    assert len(array) == 1


def test_find_nearest():
    far_coins = {Coin(32, 32), Coin(32, 64), Coin(64, 64)}
    nearest_coins = {Coin(0, 0), Coin(1, 1), Coin(16, 1), Coin(1, 16)}
    array = SlicedArray(far_coins, grid=16)
    array.multiple_append(nearest_coins)

    result = array.find_nearest(Rect(18, 18, 13, 13))
    # rect.bottom/rect.right is 31

    assert set(result) == nearest_coins


def test_iter():
    coin_a = Coin(0, 0)
    coin_b = Coin(16, 16)
    array = SlicedArray([coin_a, coin_b], grid=16)

    assert set(array) == {coin_a, coin_b}
