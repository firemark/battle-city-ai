from battle_city.monsters import Player, NPC, Bullet

from typing import List


class LogicPart(object):
    game = None  # type: battle_city.game.Game

    def __init__(self, game):
        self.game = game

    async def do_it(self):
        raise NotImplementedError('do_it')


class MoveLogicPart(LogicPart):

    async def do_it(self):
        self.move(self.game.players)
        self.move(self.game.npcs)
        self.move(self.game.bullets)

    @staticmethod
    def move(monsters):
        for monster in monsters:
            monster.move()


class PlayerTickLogicPart(LogicPart):
    ticks: int = 0

    async def do_it(self):
        self.ticks = self.ticks + 1

        if ticks > 10:
            self.ticks = 0


class CheckCollisionsLogicPart(LogicPart):

    async def do_it(self):
        players = self.game.players
        npcs = self.game.npcs
        bullets = self.game.bullets

        for player, bullet in self.check_collision(players, bullets):
            await self.remove_from_group(bullet, bullets)
            if bullet.parent_type == 'player':
                player.is_freeze = True
            else:
                await self.remove_from_group(player, players)

        for npc, bullet in self.check_collision(npcs, bullets):
            await self.remove_from_group(bullet, bullets)
            if bullet.parent_type == 'player':
                await self.remove_from_group(npc, npcs)

    async def remove_from_group(self, monster, group):
        data = dict(action='remove', id=monster.id.hex)
        group.remove(monster)
        await self.game.broadcast(data)

    @staticmethod
    def check_collision(group_a, group_b):
        for monster in group_a:
            collisions = monster.check_collision(group_b)
            for collision in collisions:
                yield (monster, collision) 


class SpawnNPCsLogicPart(LogicPart):

    async def do_it(self):
        pass


class SpawnBulletsLogicPart(LogicPart):

    async def do_it(self):
        await self.spawn_bullets(self.game.players)
        await self.spawn_bullets(self.game.npcs)

    async def spawn_bullets(self, tanks):
        for tank in tanks:
            if not tank.is_shot:
                continue
            tank.is_shot = False
            await self.spawn_bullet(tank)

    async def spawn_bullet(self, tank):
        position = tank.position
        bullet = Bullet(position.x, position.y)
        bullet.set_direction(tank.direction)
        bullet.set_parent(parent)
        bullet.move()

        data = bullet.get_serialized_data()
        data['action'] = 'spawn' 
        await self.game.broadcast(data)

        self.game.bullets.append(bullet)


class GameLogic(object):
    game = None  # type: battle_city.game.Game
    parts: List[LogicPart]

    def __init__(self, game):
        self.game = game
        self.parts = [
            # PlayerTickLogicPart(game),
            MoveLogicPart(game),
            CheckCollisionsLogicPart(game),
            # SpawnNPCsLogicPart(game),
            SpawnBulletsLogicPart(game),
        ]

    async def step(self):
        with await self.game.step_lock:
            for part in self.parts:
                await part.do_it()

