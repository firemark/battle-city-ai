from battle_city.action_handler import ActionHandler
from .utils import make_game, make_player, patch_messages

import pytest



@patch_messages
@pytest.mark.asyncio
async def test_action_greet_ok(messages):
    player = make_player()
    game = make_game(player)
    messages.get_world_data.return_value = {'action': 'foobar'}

    await ActionHandler.action_greet({'name': 'socek'}, player, game)

    messages.get_world_data.assert_called_once_with(player, game)
    player.connection.write.assert_called_once_with({
        'status': 'OK',
        'action': 'foobar',
    })

    assert player.nick == 'socek'
    assert player.ready is True
