from battle_city.monsters import Player, NPC, Bullet, Wall
from battle_city.logic import GameLogic
from battle_city.drawer import Drawer

from typing import List
from asyncio import wait, Lock


class Game(object):
    players: List[Player]
    npcs: List[NPC]
    bullets: List[Bullet]
    walls: List[Wall]
    logic: GameLogic
    drawer: Drawer
    ready: bool = False
    step_lock: Lock

    width = 512
    height = 512

    def __init__(self):
        self.players = [Player(0), Player(1)]
        self.npcs = []
        self.bullets = []
        self.walls = [
            Wall(x, 32)
            for x in range(32, self.width - 32, 32)
        ] + [
            Wall(x, 512 - 64)
            for x in range(32, self.width - 32, 32)
        ] + [
            Wall(32, y)
            for y in range(32, self.height - 32, 32)
        ] + [
            Wall(512 - 64, y)
            for y in range(32, self.height - 32, 32)
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

    async def broadcast(self, data):
        await wait([
            player.connection.write(data)
            for player in self.players
        ])

    async def send_informations(self):
        for player in self.players:
            await self.broadcast(player.get_serialized_data())
        for npc in self.npcs:
            await self.broadcast(npc.get_serialized_data())

    async def step(self):
        if self.is_ready():
            await self.logic.step()
            await self.send_informations()
        self.drawer.render()
