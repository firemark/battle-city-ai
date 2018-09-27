from typing import List

from battle_city.logic_parts.base import LogicPart
from battle_city.logic_parts.check_collision import CheckCollisionsLogicPart
from battle_city.logic_parts.move import MoveLogicPart
from battle_city.logic_parts.set_old_position import SetOldPositionLogicPart
from battle_city.logic_parts.spawn import SpawnLogicPart
from battle_city.logic_parts.tick import TickLogicPart
from battle_city.logic_parts.tick_counter import TickCounterLogicPart


class GameLogic(object):
    game = None  # type: battle_city.game.Game
    parts = None  # type: List[LogicPart]

    def __init__(self, game):
        self.game = game
        self.parts = [
            MoveLogicPart(game),
            TickLogicPart(game),
            CheckCollisionsLogicPart(game),
            SpawnLogicPart(game),
            TickCounterLogicPart(game),
            SetOldPositionLogicPart(game),
        ]

    async def step(self):
        with await self.game.step_lock:
            for part in self.parts:
                await part.do_it()

