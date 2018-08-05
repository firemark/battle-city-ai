from battle_city.monsters import Player, NPC, Bullet, Wall, Spawner
from battle_city.logic import GameLogic
from battle_city.drawer import Drawer
from battle_city.map_maker import MapMaker

from typing import List, Dict
from asyncio import wait, Lock
from itertools import chain


class Game(object):
    players: List[Player]
    npcs: List[NPC]
    bullets: List[Bullet]
    walls: List[Wall]
    player_spawns: Dict[str, Spawner]
    npc_spawns: List[Spawner]
    logic: GameLogic
    drawer: Drawer
    ready: bool = False
    step_lock: Lock
    npcs_left: int

    WIDTH = 512
    HEIGHT = 512

    MAX_NPC_IN_AREA = 5

    def __init__(self):
        self.npcs = []
        self.bullets = []
        self.walls = []
        self.player_spawns = {}
        self.npc_spawns = []
        self.players = []
        self.npcs_left = 20
        self.time_left = 300

        self.logic = GameLogic(self)
        self.drawer = None
        self.step_lock = Lock()

    def load_map(self, name):
        data_map = MapMaker.load_data_from_name(name)
        MapMaker(self, data_map).make()

        self.players = [
            Player(player_id, *self.player_spawns[player_id])
            for player_id in range(2)
        ]

    def set_drawer(self):
        self.drawer = Drawer(self)

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
