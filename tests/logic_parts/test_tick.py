from battle_city.basic import Direction
from battle_city.game import Game
from battle_city.monsters import NPC, Player
from battle_city.logic_parts.tick import TickLogicPart
from battle_city.monsters.spawner import Spawner

from asynctest import patch, DEFAULT
from unittest.mock import call


import pytest


@pytest.mark.asyncio
async def test_do_actions_after_300_ticks():
    game = Game()
    logic = TickLogicPart(game)
    game.ticks = 300

    with patch.multiple(
            logic,
            unfreeze_players=DEFAULT,
            do_it_after_ticks=DEFAULT) as patch_values:
        await logic.do_it()

    patch_values['unfreeze_players'].assert_called_once_with()
    patch_values['do_it_after_ticks'].assert_called_once_with()


@pytest.mark.asyncio
async def test_do_actions_after_10_ticks():
    game = Game()
    logic = TickLogicPart(game)
    game.ticks = 10

    with patch.multiple(
            logic,
            unfreeze_players=DEFAULT,
            do_it_after_ticks=DEFAULT) as patch_values:
        await logic.do_it()

    assert not patch_values['unfreeze_players'].called
    patch_values['do_it_after_ticks'].assert_called_once_with()


@pytest.mark.asyncio
async def test_do_it_after_ticks():
    game = Game()
    game.time_left = 250
    logic = TickLogicPart(game)

    with patch.multiple(
            logic,
            unset_player_actions=DEFAULT,
            send_info=DEFAULT,
            do_sth_with_npcs=DEFAULT) as patch_values:
        await logic.do_it_after_ticks()

    patch_values['unset_player_actions'].assert_called_once_with()
    patch_values['do_sth_with_npcs'].assert_called_once_with()
    patch_values['send_info'].assert_called_once_with()

    assert game.time_left == 249


@pytest.mark.asyncio
async def test_unfreeze_players():
    game = Game()
    game.alive_players = [Player(0, 128, 128), Player(1, 128, 128)]
    logic = TickLogicPart(game)

    await logic.unfreeze_players()

    assert not game.alive_players[0].is_freeze
    assert not game.alive_players[1].is_freeze


@pytest.mark.asyncio
@patch('battle_city.logic_parts.tick.messages')
async def test_send_info(messages):
    game = Game()
    logic = TickLogicPart(game)

    with patch.object(game, 'broadcast') as broadcast_mock:
        await logic.send_info()

    broadcast_mock.assert_called_once_with(
        messages.get_tick_game_data.return_value
    )
    messages.get_tick_game_data.assert_called_once_with(game)



# todo - check single spawn bullet with directions