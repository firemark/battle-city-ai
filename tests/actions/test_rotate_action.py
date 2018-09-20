from battle_city.server import handle_action
from battle_city.basic import Direction
from .utils import make_game, make_player

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize('raw_direction,direction', [
    ('left', Direction.LEFT),
    ('right', Direction.RIGHT),
    ('up', Direction.UP),
    ('down', Direction.DOWN),
])
async def test_action_rotate(raw_direction, direction):
    player = make_player()
    game = make_game(player)

    message = {'action': 'rotate', 'direction': raw_direction}
    await handle_action(message, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'OK',
        'direction': raw_direction,
    })

    assert player.direction is direction
    assert player.had_action is True


@pytest.mark.asyncio
async def test_action_rotate_with_wrong_direction():
    player = make_player()
    old_direction = player.direction
    game = make_game(player)

    message = {'action': 'rotate', 'direction': 'wrong'}
    await handle_action(message, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'unknown direction',
    })

    assert player.direction is old_direction
    assert player.had_action is False


@pytest.mark.asyncio
async def test_action_rotate_with_had_action():
    player = make_player(had_action=True)
    old_direction = player.direction
    game = make_game(player)

    message = {'action': 'rotate', 'direction': 'up'}
    await handle_action(message, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'too many actions per turn',
    })

    assert player.direction is old_direction
    assert player.had_action is True
