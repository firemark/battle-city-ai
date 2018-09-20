from battle_city.server import handle_action
from .utils import make_game, make_player

import pytest


@pytest.mark.asyncio
async def test_action_undefined():
    player = make_player()
    game = make_game(player)

    await handle_action({'action': 'socek'}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'unknown action',
    })
