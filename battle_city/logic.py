from typing import List

from battle_city.logic_parts.base import LogicPart
from battle_city.logic_parts.check_collision import CheckCollisionsLogicPart
from battle_city.logic_parts.move import MoveLogicPart
from battle_city.logic_parts.set_old_position import SetOldPositionLogicPart
from battle_city.logic_parts.tick import TickLogicPart


class GameLogic(object):
    game = None  # type: battle_city.game.Game
    parts = None  # type: List[LogicPart]

    def __init__(self, game):
        self.game = game
        self.parts = [
            MoveLogicPart(game),
            CheckCollisionsLogicPart(game),
            TickLogicPart(game),
            SetOldPositionLogicPart(game),
        ]

    async def step(self):
        with await self.game.step_lock:
            for part in self.parts:
                await part.do_it()

