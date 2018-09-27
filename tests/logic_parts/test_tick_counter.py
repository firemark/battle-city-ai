from battle_city.game import Game
from battle_city.logic_parts.tick_counter import TickCounterLogicPart


import pytest


@pytest.mark.asyncio
async def test_count_ticks():
    game = Game()
    logic = TickCounterLogicPart(game)
    game.ticks = 5

    await logic.do_it()

    assert game.ticks == 6


@pytest.mark.asyncio
async def test_do_actions_after_300_ticks():
    game = Game()
    logic = TickCounterLogicPart(game)
    game.ticks = 299

    await logic.do_it()

    assert game.ticks == 0
