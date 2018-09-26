from asyncio import get_event_loop

from battle_city.logic_parts.base import LogicPart
from battle_city.monsters.monster import Monster
from battle_city.monsters.player import Player

from battle_city import messages

from math import ceil, floor


class CheckCollisionsLogicPart(LogicPart):

    async def do_it(self):
        await self.check_bullets_with_player()
        await self.check_bullets_with_npc()
        await self.check_bullets_yourself()
        await self.check_bullets_with_walls()
        await self.check_tank_yourself()
        await self.check_tank_collisions_with_walls()
        await self.check_player_collisions_with_coins()

    async def check_tank_yourself(self):
        game = self.game

        tanks = list(game.get_tanks_chain())
        for tank_a, tank_b in self.check_collision(tanks, tanks):
            if tank_a is tank_b:
                continue

            # we need to check who was in this field first
            old_col_a = tank_b.check_collision_with_old_position(tank_a)
            old_col_b = tank_a.check_collision_with_old_position(tank_b)

            if old_col_a and old_col_b:
                self._move_monster_with_monster(tank_a, tank_b, 0)
                self._move_monster_with_monster(tank_a, tank_b, 1)
            elif old_col_a:
                self.move_monster_with_static_obj(tank_a, tank_b)
            elif old_col_b:
                self.move_monster_with_static_obj(tank_b, tank_a)

    def _move_monster_with_monster(self, monster_a, monster_b, axis):
        pos_a = monster_a.position[axis]
        pos_b = monster_b.position[axis]
        diff = pos_a - pos_b

        if diff > 0:
            diff -= monster_b.position[axis + 2]
        elif diff < 0:
            diff += monster_a.position[axis + 2]
        half_diff = diff / 2

        monster_a.position[axis] -= floor(half_diff)
        monster_b.position[axis] += ceil(half_diff)

    async def check_bullets_with_player(self):
        game = self.game
        players = game.alive_players
        bullets = game.bullets

        for player, bullet in self.check_collision(players, bullets):
            if bullet.parent is player:
                continue
            await self.remove_from_group(bullet, bullets)

            if isinstance(bullet.parent, Player):
                bullet.parent.score += 5
                await self.freeze(player)
            else:
                player.set_game_over()
                await self.remove_from_group(player, self.game.alive_players)

    async def check_bullets_with_npc(self):
        game = self.game
        npcs = game.npcs
        bullets = game.bullets

        for npc, bullet in self.check_collision(npcs, bullets):
            if bullet.parent is npc:
                continue

            await self.remove_from_group(bullet, bullets)
            if isinstance(bullet.parent, Player):
                bullet.parent.score += 200
                await self.remove_from_group(npc, npcs)

    async def check_bullets_yourself(self):
        game = self.game
        bullets = game.bullets

        for bullet in bullets:
            if not self.is_monster_in_area(bullet):
                await self.remove_from_group(bullet, bullets)

        for bullet_a, bullet_b in self.check_collision(bullets, bullets):
            if bullet_a is bullet_b:
                continue

            await self.remove_from_group(bullet_a, bullets)
            await self.remove_from_group(bullet_b, bullets)

    async def check_bullets_with_walls(self):
        game = self.game
        bullets = game.bullets
        walls = game.walls

        for bullet in bullets:
            with_collision_walls = bullet.check_collision_with_group(
                group=walls,
                rect=bullet.get_long_collision_rect(),
            )

            for wall in with_collision_walls:
                is_destroyed, is_touched = wall.hurt()

                if is_touched:
                    await self.remove_from_group(bullet, bullets)
                if is_destroyed:
                    await self.remove_from_group(wall, walls)
                    if isinstance(bullet.parent, Player):
                        bullet.parent.score += 1
            self.refresh_background()

    async def freeze(self, player: Player):
        player.set_freeze()
        data = messages.get_monster_serialized_data(player, action='freeze')
        await self.game.broadcast(data)

    def is_monster_in_area(self, monster):
        position = monster.position

        width = self.game.WIDTH
        height = self.game.HEIGHT

        return (
            position.left >= 0 and position.right <= width and
            position.top >= 0 and position.bottom <= height
        )

    async def check_tank_collisions_with_walls(self):
        walls = self.game.walls
        for monster in self.game.get_tanks_chain():
            # small probability to infinity loop - we need to cancel on 5th try
            for i in range(5):
                # check_collision is very greedy - in future we need quadtree structure
                collision_walls = monster.check_collision_with_group(walls)
                if not collision_walls:
                    break
                wall = collision_walls[0]
                self.move_monster_with_static_obj(monster, wall)

        for monster in self.game.get_tanks_chain():
            if monster.position.left < 0:
                monster.position.x = 0
            elif monster.position.right > self.game.WIDTH:
                monster.position.x = self.game.WIDTH - monster.SIZE

            if monster.position.top < 0:
                monster.position.y = 0
            elif monster.position.bottom > self.game.HEIGHT:
                monster.position.y = self.game.HEIGHT - monster.SIZE

    async def check_player_collisions_with_coins(self):
        players = self.game.alive_players
        coins = self.game.coins

        for player, coin in self.check_collision(players, coins):
            await self.remove_from_group(coin, self.game.coins)
            player.score += 100
            self.refresh_background()

    @classmethod
    def move_monster_with_static_obj(cls, monster, other):
        cls.move_monster_with_static_obj_axis(monster, other, axis=0)
        cls.move_monster_with_static_obj_axis(monster, other, axis=1)

    @staticmethod
    def get_border_diff(pos_a, pos_b, axis: int) -> int:
        """
        :return: for axis=0 A.left - B.right, for axis=1 A.top - B.bottom

        """
        return pos_a[axis] - pos_b[axis] - pos_b[axis + 2]

    @classmethod
    def move_monster_with_static_obj_axis(
            cls, monster: Monster, other: Monster, axis: int):
        monster_pos = monster.position
        other_pos = other.position

        # we need to detect direction of move using diff
        diff = monster.position[axis] - monster.old_position[axis]

        # according to diff we can move monster to selected side of other
        if diff > 0:
            monster_pos[axis] += cls.get_border_diff(other_pos, monster_pos, axis)
        elif diff < 0:
            monster_pos[axis] -= cls.get_border_diff(monster_pos, other_pos, axis)

    def refresh_background(self):
        if not self.game.drawer:
            return
        loop = get_event_loop()
        loop.call_soon(self.game.drawer.bake_static_background)

    async def remove_from_group(self, monster, group):
        try:
            group.remove(monster)
        except ValueError:
            return

        data = messages.get_remove_monster_data(monster)
        await self.game.broadcast(data)

    @staticmethod
    def check_collision(group_a, group_b):
        for monster in group_a:
            collisions = monster.check_collision_with_group(group_b)
            for collision in collisions:
                yield (monster, collision)
