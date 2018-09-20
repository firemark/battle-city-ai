from battle_city.server import handle_action
from .utils import make_game, make_player

import pytest


@pytest.mark.asyncio
async def test_action_shoot():
    player = make_player()
    game = make_game(player)

    await handle_action({'action': 'shoot'}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'OK',
    })

    assert player.is_shot is True
    assert player.had_action is True


@pytest.mark.asyncio
async def test_action_shoot_when_had_action():
    player = make_player(had_action=True)
    game = make_game(player)

    await handle_action({'action': 'shoot'}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'too many actions per turn',
    })

    assert player.is_shot is False
