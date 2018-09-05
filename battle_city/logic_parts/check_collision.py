from battle_city.logic_parts.base import LogicPart
from battle_city.monsters.monster import Monster
from battle_city.monsters.player import Player

from battle_city import messages


class CheckCollisionsLogicPart(LogicPart):

    async def do_it(self):
        game = self.game
        players = game.alive_players
        npcs = game.npcs
        bullets = game.bullets
        walls = game.walls

        for player, bullet in self.check_collision(players, bullets):
            await self.remove_from_group(bullet, bullets)
            if bullet.parent_type == 'player':
                bullet.parent.score += 5
                await self.freeze(player)
            else:
                player.set_game_over()
                await self.remove_from_group(player, self.game.alive_players)

        for npc, bullet in self.check_collision(npcs, bullets):
            await self.remove_from_group(bullet, bullets)
            if bullet.parent_type == 'player':
                bullet.parent.score += 200
                await self.remove_from_group(npc, npcs)

        for bullet in bullets:
            if not self.is_monster_in_area(bullet):
                await self.remove_from_group(bullet, bullets)

        for bullet_a, bullet_b in self.check_collision(bullets, bullets):
            if bullet_a is bullet_b:
                continue

            await self.remove_from_group(bullet_a, bullets)
            await self.remove_from_group(bullet_b, bullets)

        for bullet, wall in self.check_collision(bullets, walls):
            is_destroyed, is_touched = wall.hurt(bullet.direction)

            if is_touched:
                await self.remove_from_group(bullet, bullets)

            if is_destroyed:

                walls_to_destroy = bullet.check_collision_with_group(
                    group=walls,
                    rect=bullet.get_long_collision_rect(),
                )
                for wall_to_destroy in walls_to_destroy:
                    await self.remove_from_group(wall_to_destroy, walls)

                    if bullet.parent_type == 'player':
                        bullet.parent.score += 1

        tanks = list(self.game.get_tanks_chain())
        for tank_a, tank_b in self.check_collision(tanks, tanks):
            if tank_a is tank_b:
                continue

            # we need to check who was in this field first
            if not tank_a.check_collision_with_old_position(tank_b):
                self.move_monster_with_static_obj(tank_a, tank_b)
            else:
                self.move_monster_with_static_obj(tank_b, tank_a)

        self.check_tank_collisions(players)
        self.check_tank_collisions(npcs)

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

    def check_tank_collisions(self, monsters):
        walls = self.game.walls
        for monster in monsters:
            # small probability to infinity loop - we need to cancel on 5th try
            for i in range(5):
                # check_collision is very greedy - in future we need quadtree structure
                collision_walls = monster.check_collision_with_group(walls)
                if not collision_walls:
                    break
                wall = collision_walls[0]
                self.move_monster_with_static_obj(monster, wall)

        for monster in monsters:
            if monster.position.left < 0:
                monster.position.x = 0
            elif monster.position.right > self.game.WIDTH:
                monster.position.x = self.game.WIDTH - monster.SIZE

            if monster.position.top < 0:
                monster.position.y = 0
            elif monster.position.bottom > self.game.HEIGHT:
                monster.position.y = self.game.HEIGHT - monster.SIZE

    @classmethod
    def move_monster_with_static_obj(cls, monster, other):
        cls.move_monster_with_static_obj_axis(monster, other, axis=0)
        cls.move_monster_with_static_obj_axis(monster, other, axis=1)

    @classmethod
    def move_monster_with_monster(cls, monster, other):
        # probably will be removed in future
        cls.move_monster_with_monster_axis(monster, other, axis=0)
        cls.move_monster_with_monster_axis(monster, other, axis=1)

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

    @classmethod
    def move_monster_with_monster_axis(
            cls, monster: Monster, other: Monster, axis: int):
        monster_pos = monster.position
        other_pos = other.position

        # we need to detect direction of move using diff
        diff_mon = monster.position[axis] - monster.old_position[axis]
        diff_oth = other.position[axis] - other.old_position[axis]

        if diff_mon == 0:
            return cls.move_monster_with_static_obj_axis(other, monster, axis)
        elif diff_oth == 0:
            return cls.move_monster_with_static_obj_axis(monster, other, axis)

        sign_mon = diff_mon > 0
        sign_oth = diff_oth > 0

        if sign_mon != sign_oth:
            if sign_mon:
                delta = cls.get_border_diff(other_pos, monster_pos, axis)
                half_delta = delta // 2  # remember about round integers
                monster_pos[axis] += half_delta
                other_pos[axis] -= delta - half_delta
            else:
                delta = cls.get_border_diff(monster_pos, other_pos, axis)
                half_delta = delta // 2  # remember about round integers
                monster_pos[axis] -= half_delta
                other_pos[axis] += delta - half_delta
        else:
            if diff_mon > diff_oth:
                monster_pos[axis] -= diff_mon - diff_oth
            else:
                other_pos[axis] -= diff_oth - diff_mon

    async def remove_from_group(self, monster, group):
        try:
            group.remove(monster)
        except ValueError:
            return

        data = dict(status='data', action='destroy', id=monster.id.hex)
        await self.game.broadcast(data)

    @staticmethod
    def check_collision(group_a, group_b):
        for monster in group_a:
            collisions = monster.check_collision_with_group(group_b)
            for collision in collisions:
                yield (monster, collision)
