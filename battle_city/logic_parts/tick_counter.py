from battle_city.logic_parts.base import LogicPart


class TickCounterLogicPart(LogicPart):
    ticks = 0

    async def do_it(self):
        self.game.ticks += 1

        if self.game.ticks >= 300:
            self.game.ticks = 0
