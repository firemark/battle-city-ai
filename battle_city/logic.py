from battle_city.monsters import Player, NPC, Bullet

from typing import List


class GameLogic(object):
    game = None  # type: Game

    def __init__(self, game):
        self.game = game

    async def step(self):
        await self.move_monsters()
        await self.check_collisions()
        await self.spawn()

    async def move_monsters(self):
        game = self.game
        self._move(game.players)
        self._move(game.npcs)
        self._move(game.bullets)

    @staticmethod
    def _move(monsters):
        for monster in monsters:
            monster.move()

    async def check_collisions(self):
        players = self.game.players
        npcs = self.game.npcs
        bullets = self.game.bullets

        for player, bullet in self._check_collision(players, bullets):
            await self._remove_from_group(bullet, bullets)
            if bullet.parent_type == 'player':
                player.is_freeze = True
            else:
                await self._remove_from_group(player, players)

        for npc, bullet in self._check_collision(npcs, bullets):
            await self._remove_from_group(bullet, bullets)
            if bullet.parent_type == 'player':
                await self._remove_from_group(npc, npcs)

    async def _remove_from_group(self, monster, group):
        data = dict(action='remove', id=monster.id.hex)
        group.remove(monster)
        await self.game.broadcast(data)

    @staticmethod
    def _check_collision(group_a, group_b):
        for monster in group_a:
            collisions = monster.check_collision(group_b)
            for collision in collisions:
                yield (monster, collision) 

    async def spawn(self):
        await self._spawn_bullets(self.game.players)
        await self._spawn_bullets(self.game.npcs)

    async def _spawn_bullets(self, tanks):
        for tank in tanks:
            if not tank.is_shot:
                continue
            tank.is_shot = False
            await self._spawn_bullet(tank)

    async def _spawn_bullet(self, tank):
        position = tank.position
        bullet = Bullet(position.x, position.y)
        bullet.set_direction(tank.direction)
        bullet.set_parent(parent)
        bullet.move()

        data = bullet.get_serialized_data()
        data['action'] = 'spawn' 
        await self.game.broadcast(data)

        self.game.bullets.append(bullet)
