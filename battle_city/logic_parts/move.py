from battle_city.logic_parts.base import LogicPart


class MoveLogicPart(LogicPart):

    async def do_it(self):
        for monster in self.game.get_monsters_chain():
            monster.move()
