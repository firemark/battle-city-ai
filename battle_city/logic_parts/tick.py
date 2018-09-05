from battle_city.basic import Direction
from battle_city.logic_parts.base import LogicPart
from battle_city.monsters.bullet import Bullet
from battle_city.monsters.npc import NPC
from battle_city import messages


from random import random, choice


class TickLogicPart(LogicPart):
    ticks: int = 0

    async def do_it(self):
        self.ticks += 1

        if self.ticks >= 300:
            self.ticks = 0
            await self.unfreeze_players()

        if self.ticks % 10 == 0:
            await self.do_it_after_ticks()

    async def unfreeze_players(self):
        for player in self.game.alive_players:
            player.unset_freeze()

    async def do_it_after_ticks(self):
        await self.unset_player_actions()
        await self.spawn_bullets()
        await self.spawn_npc()
        await self.do_sth_with_npcs()

        self.game.time_left -= 1

    async def unset_player_actions(self):
        for player in self.game.alive_players:
            player.had_action = False

    async def spawn_bullets(self):
        for tank in self.game.get_tanks_chain():
            if not tank.is_shot:
                continue
            tank.is_shot = False
            await self.spawn_bullet(tank)

    async def spawn_bullet(self, tank):
        position = tank.position
        direction = tank.direction

        size = Bullet.SIZE
        half_size = size // 2

        if direction is Direction.UP:
            x = position.centerx - half_size
            y = position.top - size
        elif direction is Direction.DOWN:
            x = position.centerx - half_size
            y = position.bottom + size
        elif direction is Direction.LEFT:
            x = position.left - size
            y = position.centery - half_size
        elif direction is Direction.RIGHT:
            x = position.right + size
            y = position.centery - half_size
        else:
            x = 0
            y = 0

        bullet = Bullet(x, y)
        bullet.set_direction(direction)
        bullet.set_parent(tank)

        data = messages.get_monster_serialized_data(bullet, action='spawn')
        await self.game.broadcast(data)

        self.game.bullets.append(bullet)

    async def spawn_npc(self):
        if len(self.game.npcs) >= self.game.MAX_NPC_IN_AREA:
            return
        if random() > 0.6 / (len(self.game.npcs) + 1):
            return

        spawn = choice(self.game.npc_spawns)
        npc = NPC(*spawn)
        self.game.npcs.append(npc)
        self.game.npcs_left -= 1
        npc_data = messages.get_monster_serialized_data(npc, action='spawn')
        await self.game.broadcast(npc_data)

    async def do_sth_with_npcs(self):
        for npc in self.game.npcs:
            is_changed = npc.do_something()
            if not is_changed:
                continue
            npc_data = messages.get_monster_serialized_data(npc)
            await self.game.broadcast(npc_data)
