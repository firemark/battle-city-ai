from battle_city.server import handle_action
from .utils import make_game, make_player

import pytest


@pytest.mark.asyncio
async def test_action_set_speed():
    player = make_player()
    game = make_game(player)

    await handle_action({'action': 'set_speed', 'speed': 2}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'OK',
        'speed': 2,
    })

    assert player.speed == 2
    assert player.had_action is True


@pytest.mark.asyncio
async def test_action_set_speed_bigger_than_two():
    player = make_player()
    game = make_game(player)

    await handle_action({'action': 'set_speed', 'speed': 123}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'OK',
        'speed': 2,
    })

    assert player.speed == 2
    assert player.had_action is True


@pytest.mark.asyncio
async def test_action_set_speed_lower_than_zero():
    player = make_player()
    game = make_game(player)

    await handle_action({'action': 'set_speed', 'speed': -123}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'OK',
        'speed': 0,
    })

    assert player.speed == 0
    assert player.had_action is True


@pytest.mark.asyncio
async def test_action_set_speed_not_int():
    player = make_player()
    game = make_game(player)

    await handle_action({'action': 'set_speed', 'speed': 1.23}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'speed has wrong value',
    })

    assert player.had_action is False


@pytest.mark.asyncio
async def test_action_set_speed_when_had_action():
    player = make_player(had_action=True)
    game = make_game(player)

    await handle_action({'action': 'set_speed', 'speed': 2}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'too many actions per turn',
    })

    assert player.speed == 0
