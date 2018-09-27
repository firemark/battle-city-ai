from battle_city.basic import Direction
from battle_city.game import Game
from battle_city.logic_parts.spawn import SpawnLogicPart
from battle_city.monsters import NPC, Player
from battle_city.monsters.spawner import Spawner

from asynctest import patch, DEFAULT
from unittest.mock import call


import pytest


@pytest.mark.asyncio
async def test_do_actions_after_10_ticks():
    game = Game()
    logic = SpawnLogicPart(game)
    game.ticks = 10

    with patch.multiple(
            logic,
            do_it_after_ticks=DEFAULT) as patch_values:
        await logic.do_it()

    patch_values['do_it_after_ticks'].assert_called_once_with()


@pytest.mark.asyncio
async def test_do_it_after_ticks():
    game = Game()
    logic = SpawnLogicPart(game)

    with patch.multiple(
            logic,
            spawn_bullets=DEFAULT,
            spawn_npc=DEFAULT) as patch_values:
        await logic.do_it_after_ticks()

    patch_values['spawn_npc'].assert_called_once_with()
    patch_values['spawn_bullets'].assert_called_once_with()


@pytest.mark.asyncio
@patch('battle_city.logic_parts.spawn.messages')
async def test_spawn_bullets(messages):
    game = Game()
    game.alive_players = [Player(0, 128, 128)]
    game.npcs = [NPC(128, 128)]
    logic = SpawnLogicPart(game)

    game.alive_players[0].set_direction(Direction.DOWN)
    game.npcs[0].set_direction(Direction.LEFT)

    game.alive_players[0].set_shot()
    game.npcs[0].set_shot()

    with patch.object(game, 'broadcast') as broadcast_mock:
        await logic.spawn_bullets()

    assert not game.alive_players[0].is_shot
    assert not game.npcs[0].is_shot

    player_bullet, npc_bullet = game.bullets

    assert player_bullet.parent is game.alive_players[0]
    assert player_bullet.direction == Direction.DOWN
    assert player_bullet.get_position() == {'x': 128 + 16 - 2, 'y': 152}

    assert npc_bullet.parent is game.npcs[0]
    assert npc_bullet.direction == Direction.LEFT
    assert npc_bullet.get_position() == {'x': 136, 'y': 128 + 16 - 2}

    assert broadcast_mock.call_args_list == [
        call(messages.get_monster_serialized_data.return_value),
        call(messages.get_monster_serialized_data.return_value),
    ]

    assert messages.get_monster_serialized_data.call_args_list == [
        call(player_bullet, action='spawn'),
        call(npc_bullet, action='spawn'),
    ]


@pytest.mark.asyncio
@patch('battle_city.logic_parts.spawn.random')
@patch('battle_city.logic_parts.spawn.messages')
async def test_spawn_npc(messages, random_mock):
    game = Game()
    game.npc_spawns = [Spawner(x=128, y=128)]
    logic = SpawnLogicPart(game)
    random_mock.return_value = 0.0

    with patch.object(game, 'broadcast') as broadcast_mock:
        await logic.spawn_npc()

    npc = game.npcs[0]
    assert npc.get_position() == {'x': 128, 'y': 128}

    broadcast_mock.assert_called_once_with(
        messages.get_monster_serialized_data.return_value
    )
    messages.get_monster_serialized_data.assert_called_once_with(npc, action='spawn')


# todo - check single spawn bullet with directions
