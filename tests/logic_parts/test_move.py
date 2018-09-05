from battle_city.game import Game
from battle_city.monsters import Bullet, NPC, Player
from battle_city.logic_parts.move import MoveLogicPart

import pytest


@pytest.mark.asyncio
async def test_move():
    game = Game()

    # default direction is UP
    game.bullets = [Bullet(128, 128)]
    game.players = [Player(x=128, y=128, player_id=0)]

    # but default direction of NPC is DOWN
    game.npcs = [NPC(128, 128)]

    game.players[0].set_speed(2)
    game.npcs[0].set_speed(2)

    await MoveLogicPart(game).do_it()

    assert game.players[0].get_position() == {'x': 128, 'y': 128 - 2}
    assert game.npcs[0].get_position() == {'x': 128, 'y': 128 + 2}
    assert game.bullets[0].get_position() == {'x': 128, 'y': 128 - 10}
