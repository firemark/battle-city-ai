from battle_city.basic import Direction
from battle_city.game import Game
from battle_city.monsters import NPC, Player
from battle_city.logic_parts.tick import TickLogicPart

import pytest

from asynctest import patch, DEFAULT

from battle_city.monsters.spawner import Spawner


@pytest.mark.asyncio
async def test_count_ticks():
    game = Game()
    logic = TickLogicPart(game)
    logic.ticks = 5

    await logic.do_it()

    assert logic.ticks == 6


@pytest.mark.asyncio
async def test_do_actions_after_300_ticks():
    game = Game()
    logic = TickLogicPart(game)
    logic.ticks = 299

    with patch.multiple(
            logic,
            unfreeze_players=DEFAULT,
            do_it_after_ticks=DEFAULT) as patch_values:
        await logic.do_it()

    assert logic.ticks == 0

    patch_values['unfreeze_players'].assert_called_once_with()
    patch_values['do_it_after_ticks'].assert_called_once_with()


@pytest.mark.asyncio
async def test_do_actions_after_10_ticks():
    game = Game()
    logic = TickLogicPart(game)
    logic.ticks = 9

    with patch.multiple(
            logic,
            unfreeze_players=DEFAULT,
            do_it_after_ticks=DEFAULT) as patch_values:
        await logic.do_it()

    assert logic.ticks == 10

    assert not patch_values['unfreeze_players'].called
    patch_values['do_it_after_ticks'].assert_called_once_with()


@pytest.mark.asyncio
async def test_do_it_after_ticks():
    game = Game()
    game.time_left = 250
    game.players = [Player(0, 128, 128)]
    game.npcs = [NPC(128, 128)]
    logic = TickLogicPart(game)

    with patch.multiple(
            logic,
            spawn_bullets=DEFAULT,
            spawn_npc=DEFAULT,
            unset_player_actions=DEFAULT,
            do_sth_with_npcs=DEFAULT) as patch_values:
        await logic.do_it_after_ticks()

    patch_values['unset_player_actions'].assert_called_once_with()
    patch_values['spawn_npc'].assert_called_once_with()
    patch_values['do_sth_with_npcs'].assert_called_once_with()
    patch_values['spawn_bullets'].assert_called_once_with()

    assert game.time_left == 249


@pytest.mark.asyncio
async def test_unfreeze_players():
    game = Game()
    game.players = [Player(0, 128, 128), Player(1, 128, 128)]
    logic = TickLogicPart(game)

    await logic.unfreeze_players()

    assert not game.players[0].is_freeze
    assert not game.players[1].is_freeze


@pytest.mark.asyncio
async def test_unset_player_actions():
    game = Game()
    game.players = [Player(0, 128, 128), Player(1, 128, 128)]
    for player in game.players:
        player.set_had_action()

    logic = TickLogicPart(game)

    await logic.unset_player_actions()

    assert not game.players[0].had_action
    assert not game.players[1].had_action


@pytest.mark.asyncio
async def test_spawn_bullets():
    game = Game()
    game.players = [Player(0, 128, 128)]
    game.npcs = [NPC(128, 128)]
    logic = TickLogicPart(game)

    game.players[0].set_direction(Direction.DOWN)
    game.npcs[0].set_direction(Direction.LEFT)

    game.players[0].set_shot()
    game.npcs[0].set_shot()

    with patch.object(game, 'broadcast') as broadcast_mock:
        await logic.spawn_bullets()

    assert not game.players[0].is_shot
    assert not game.npcs[0].is_shot

    player_bullet, npc_bullet = game.bullets

    assert player_bullet.parent_id is game.players[0].id
    assert player_bullet.direction == Direction.DOWN
    assert player_bullet.get_position() == {'x': 128 + 16 - 2, 'y': 128 + 32 + 4}

    assert npc_bullet.parent_id is game.npcs[0].id
    assert npc_bullet.direction == Direction.LEFT
    assert npc_bullet.get_position() == {'x': 128 - 4, 'y': 128 + 16 - 2}

    assert broadcast_mock.call_count == 2


@pytest.mark.asyncio
@patch('battle_city.logic.random')
async def test_spawn_npc(random_mock):
    game = Game()
    game.npc_spawns = [Spawner(x=128, y=128)]
    logic = TickLogicPart(game)
    random_mock.return_value = 0.0

    with patch.object(game, 'broadcast') as broadcast_mock:
        await logic.spawn_npc()

    npc = game.npcs[0]
    assert npc.get_position() == {'x': 128, 'y': 128}

    broadcast_mock.assert_called_once_with(dict(
        status='data',
        action='spawn',
        id=npc.id.hex,
        type='npc',
        speed=2,
        position={'x': 128, 'y': 128},
        is_freeze=False,
        direction='down',
    ))


# todo - check single spawn bullet with directions