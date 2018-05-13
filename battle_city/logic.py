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


class TickLogicPart(LogicPart):
    ticks: int = 0

    async def do_it(self):
        self.ticks = self.ticks + 1

        if self.ticks >= 300:
            self.ticks = 0
            await self.unfreeze_players()

        if self.ticks % 10 == 0:
            await self.do_it_after_ticks()

    async def unfreeze_players(self):
        for player in self.game.players:
            player.is_freeze = False
            
    async def do_it_after_ticks(self):
        for player in self.game.players:
            player.had_action = False
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
        bullet = Bullet(
            x=position.centerx,
            y=position.centery,
        )
        bullet.set_direction(tank.direction)
        bullet.set_parent(tank)
        bullet.move_with_speed(32 - bullet.speed)

        data = bullet.get_serialized_data()
        data['action'] = 'spawn' 
        await self.game.broadcast(data)

        self.game.bullets.append(bullet)


class CheckCollisionsLogicPart(LogicPart):

    async def do_it(self):
        game = self.game
        players = game.players
        npcs = game.npcs
        bullets = game.bullets
        walls = game.walls

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

        for bullet in bullets:
            if not self.is_monster_in_area(bullet):
                await self.remove_from_group(bullet, bullets)

        for bullet, wall in self.check_collision(bullets, walls):
            await self.remove_from_group(bullet, bullets)
            wall.hurt(bullet.direction)
            if wall.is_destroyed:
                await self.remove_from_group(wall, walls)
                
        self.check_tank_collision_with_walls(players)
        self.check_tank_collision_with_walls(npcs)

    def is_monster_in_area(self, monster): 
        position = monster.position

        width = self.game.width
        height = self.game.height

        return (
            position.left >= 0 and position.right <= width and
            position.top >= 0 and position.bottom <= height
        )

    def check_tank_collision_with_walls(self, monsters):
        walls = self.game.walls
        for monster, wall in self.check_collision(monsters, walls):
            monster.move_with_speed(-monster.speed)

        for monster in monsters:
            if not self.is_monster_in_area(monster):
                monster.move_with_speed(-monster.speed)

    async def remove_from_group(self, monster, group):
        data = dict(action='remove', id=monster.id.hex)
        try:
            group.remove(monster)
        except ValueError:
            pass
        else:
            await self.game.broadcast(data)

    @staticmethod
    def check_collision(group_a, group_b):
        for monster in group_a:
            collisions = monster.check_collision(group_b)
            for collision in collisions:
                yield (monster, collision) 


class GameLogic(object):
    game = None  # type: battle_city.game.Game
    parts: List[LogicPart]

    def __init__(self, game):
        self.game = game
        self.parts = [
            TickLogicPart(game),
            MoveLogicPart(game),
            CheckCollisionsLogicPart(game),
        ]

    async def step(self):
        with await self.game.step_lock:
            for part in self.parts:
                await part.do_it()

