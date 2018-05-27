from battle_city.monsters import Player, NPC, Bullet, Wall
from battle_city.logic import GameLogic
from battle_city.drawer import Drawer

from typing import List
from asyncio import wait, Lock
from itertools import chain


class Game(object):
    players: List[Player]
    npcs: List[NPC]
    bullets: List[Bullet]
    walls: List[Wall]
    logic: GameLogic
    drawer: Drawer
    ready: bool = False
    step_lock: Lock

    WIDTH = 512
    HEIGHT = 512

    MAX_NPC_IN_AREA = 3

    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.npcs = []
        self.bullets = []
        self.walls = [
            Wall(x, 32)
            for x in range(32, self.WIDTH - 32, 32)
        ] + [
            Wall(x, 512 - 64)
            for x in range(32, self.WIDTH - 32, 32)
        ] + [
            Wall(32, y)
            for y in range(32, self.HEIGHT - 32, 32)
        ] + [
            Wall(512 - 64, y)
            for y in range(32, self.HEIGHT - 32, 32)
        ]
        self.logic = GameLogic(self)
        self.drawer = Drawer(self)
        self.step_lock = Lock()

    def set_next_player(self, connection):
        for player in self.players:
            if player.ready:
                continue
            player.set(connection)
            return player 
        else:
            return None

    def is_ready(self):
        if len(self.players) < 2:
            return False
        return all(player.ready for player in self.players)

    def run(self):
        self.ready = True

    def get_monsters_chain(self):
        return chain(
            self.players,
            self.npcs,
            self.bullets,
        )

    def get_tanks_chain(self):
        return chain(self.players, self.npcs)

    async def broadcast(self, data):
        await wait([
            player.connection.write(data)
            for player in self.players
            if player.connection is not None
        ])

    async def send_informations(self):
        for monster in self.get_monsters_chain():
            data = monster.get_serialized_move_data()
            await self.broadcast(data)

    async def step(self):
        if self.is_ready():
            await self.logic.step()
            await self.send_informations()
        self.drawer.render()
