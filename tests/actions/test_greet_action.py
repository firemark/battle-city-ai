from battle_city.action_handler import ActionHandler
from .utils import make_game, make_player, patch_messages
from asynctest.mock import patch
import pytest

patch_messages = patch('battle_city.action_handler.messages')


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


@pytest.mark.asyncio
async def test_action_greet_with_blank_name():
    player = make_player()
    game = make_game(player)

    await ActionHandler.action_greet({'name': ''}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'name is blank',
    })


@pytest.mark.asyncio
async def test_action_greet_with_undefined_name():
    player = make_player()
    game = make_game(player)

    await ActionHandler.action_greet({}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'name is undefined',
    })


@pytest.mark.asyncio
async def test_action_greet_with_wrong_type_name():
    player = make_player()
    game = make_game(player)

    await ActionHandler.action_greet({'name': 123}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'name has wrong type',
    })


@pytest.mark.asyncio
async def test_action_greet_with_too_long_name():
    player = make_player()
    game = make_game(player)

    await ActionHandler.action_greet({'name': 'a' * 50}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'name is too long (max is 10)',
    })


@pytest.mark.asyncio
async def test_action_greet_again():
    player = make_player()
    player.ready = True
    game = make_game(player)

    await ActionHandler.action_greet({'name': 'a'}, player, game)

    player.connection.write.assert_called_once_with({
        'status': 'ERROR',
        'message': 'you are greeted before',
    })
