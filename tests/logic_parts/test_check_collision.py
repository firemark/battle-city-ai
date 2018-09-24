from battle_city.game import Game
from battle_city.monsters import Player, NPC, Bullet
from battle_city.logic_parts.check_collision import CheckCollisionsLogicPart

from unittest.mock import patch, Mock, call
from asynctest.mock import Mock as AsyncMock

import pytest


@pytest.mark.asyncio
async def test_do_it():
    logic = AsyncMock(CheckCollisionsLogicPart(None))

    await CheckCollisionsLogicPart.do_it(logic)

    assert logic.method_calls == [
        call.check_bullets_with_player(),
        call.check_bullets_with_npc(),
        call.check_bullets_yourself(),
        call.check_bullets_with_walls(),
        call.check_tank_yourself(),
        call.check_tank_collisions_with_walls(),
    ]


@pytest.mark.asyncio
async def test_check_two_tanks_with_one_collision():
    game = Game()
    # size of tanks are 32x32
    game.alive_players = [Player(0, 0, 0)]
    game.alive_players[0].set_position(32, 0)  # collision!
    game.npcs = [NPC(48, 0)]

    logic = CheckCollisionsLogicPart(game)

    await logic.check_tank_yourself()

    assert game.npcs[0].get_position() == {'x': 48, 'y': 0}
    assert game.alive_players[0].get_position() == {'x': 16, 'y': 0}


@pytest.mark.asyncio
async def test_check_two_tanks_with_both_collision():
    game = Game()
    # size of tanks are 32x32
    game.alive_players = [Player(0, 0, 0)]
    game.npcs = [NPC(32, 0)]

    game.alive_players[0].set_position(4, 0)  # collision!
    game.npcs[0].set_position(28, 0)  # collision too!
    # diff is 8

    logic = CheckCollisionsLogicPart(game)

    await logic.check_tank_yourself()

    assert game.npcs[0].get_position() == {'x': 28 + 4, 'y': 0}
    assert game.alive_players[0].get_position() == {'x': 4 - 4, 'y': 0}


@pytest.mark.parametrize('reverse', [True, False])
def test_move_monster_with_monster(reverse):
    game = Game()
    # size of tanks are 32x32
    player = Player(0, 0, 0)
    npc = NPC(32, 0)

    player.set_position(4, 0)  # collision!
    npc.set_position(28, 0)  # collision too!
    # diff is 8

    logic = CheckCollisionsLogicPart(game)
    if reverse:
        logic._move_monster_with_monster(player, npc, axis=0)
    else:
        logic._move_monster_with_monster(npc, player, axis=0)

    assert npc.get_position() == {'x': 28 + 4, 'y': 0}
    assert player.get_position() == {'x': 4 - 4, 'y': 0}


@pytest.mark.asyncio
async def test_check_freeze_player_with_bullet_collision():
    game = Game()
    player = Player(0, 0, 0)
    attacker = Player(1, 64, 64)
    game.alive_players = [player, attacker]
    game.bullets = [Bullet(0, 0)]
    game.bullets[0].set_parent(attacker)

    logic = CheckCollisionsLogicPart(game)
    await logic.check_bullets_with_player()

    assert len(game.bullets) == 0
    assert player.is_freeze is True
    assert attacker.score == 5


@pytest.mark.asyncio
async def test_check_destroy_player_with_bullet_collision():
    game = Game()
    player = Player(0, 0, 0)
    attacker = NPC(64, 64)
    game.alive_players = [player]
    game.npcs = [attacker]
    game.bullets = [Bullet(0, 0)]
    game.bullets[0].set_parent(attacker)

    logic = CheckCollisionsLogicPart(game)
    await logic.check_bullets_with_player()

    assert len(game.bullets) == 0
    assert len(game.players) == 0


@pytest.mark.asyncio
async def test_check_destroy_npc_with_bullet_collision():
    game = Game()
    player = Player(0, 0, 0)
    game.npcs = [NPC(0, 0)]
    game.bullets = [Bullet(0, 0)]
    game.bullets[0].set_parent(player)

    logic = CheckCollisionsLogicPart(game)
    await logic.check_bullets_with_npc()

    assert len(game.bullets) == 0
    assert len(game.npcs) == 0
    assert player.score == 200


@pytest.mark.asyncio
async def test_check_npc_with_another_npc_bullet_collision():
    game = Game()
    attacker = NPC(64, 64)
    game.npcs = [NPC(0, 0), attacker]
    game.bullets = [Bullet(0, 0)]
    game.bullets[0].set_parent(attacker)

    logic = CheckCollisionsLogicPart(game)
    await logic.check_bullets_with_npc()

    assert len(game.bullets) == 0
    assert len(game.npcs) == 2


@pytest.mark.asyncio
async def test_check_bullet_both_collision():
    game = Game()
    game.bullets = [Bullet(0, 0), Bullet(0, 0), Bullet(-30, 0)]

    logic = CheckCollisionsLogicPart(game)
    await logic.check_bullets_yourself()

    assert len(game.bullets) == 0
