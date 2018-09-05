from battle_city.logic_parts.base import LogicPart


class SetOldPositionLogicPart(LogicPart):

    async def do_it(self):
        for monster in self.game.get_monsters_chain():
            monster.set_old_position()
