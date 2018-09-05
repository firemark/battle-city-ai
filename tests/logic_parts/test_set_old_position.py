from battle_city.game import Game
from battle_city.monsters import Bullet, NPC, Player
from battle_city.logic_parts.set_old_position import SetOldPositionLogicPart

import pytest


@pytest.mark.asyncio
async def test_set_old_position():
    game = Game()
    game.bullets = [Bullet(128, 128)]
    game.players = [Player(x=128, y=128, player_id=0)]
    game.npcs = [NPC(128, 128)]

    for monster in game.get_monsters_chain():
        monster.set_position(42, 24)

    await SetOldPositionLogicPart(game).do_it()

    for monster in game.bullets + game.players + game.npcs:
        assert monster.old_position.x == 42
        assert monster.old_position.y == 24
