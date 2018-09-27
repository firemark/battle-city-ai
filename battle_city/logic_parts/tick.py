from battle_city.logic_parts.base import LogicPart
from battle_city import messages


class TickLogicPart(LogicPart):

    async def do_it(self):
        if self.game.ticks >= 300:
            await self.unfreeze_players()

        if self.game.ticks % 10 == 0:
            await self.do_it_after_ticks()

    async def unfreeze_players(self):
        for player in self.game.alive_players:
            player.unset_freeze()

    async def do_it_after_ticks(self):
        await self.unset_player_actions()
        await self.do_sth_with_npcs()
        await self.send_info()

        self.game.time_left -= 1

    async def send_info(self):
        data = messages.get_tick_game_data(self.game)
        await self.game.broadcast(data)

    async def unset_player_actions(self):
        for player in self.game.alive_players:
            player.had_action = False

    async def do_sth_with_npcs(self):
        for npc in self.game.npcs:
            is_changed = npc.do_something()
            if not is_changed:
                continue
            npc_data = messages.get_monster_serialized_data(npc)
            await self.game.broadcast(npc_data)
