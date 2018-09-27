from battle_city.monsters import Player, NPC, Bullet, Wall, Spawner
from battle_city.logic import GameLogic
from battle_city.drawer import Drawer
from battle_city.map_maker import MapMaker

from battle_city import messages

from typing import List, Dict
from asyncio import wait, Lock
from itertools import chain


class Game(object):
    players = None  # type: List[Player]
    npcs = None  # type:  List[NPC]
    bullets = None # type: List[Bullet]
    walls = None  # type: List[Wall]
    coins = None  # type: List[Coin]
    player_spawns = None  # type: Dict[str, Spawner]
    npc_spawns = None  # type: List[Spawner]
    logic = None  # type: GameLogic
    drawer = None  # type: Drawer
    ready = False  # type: False
    step_lock = None  # type: Lock
    npcs_left = 0  # type: int
    ticks = 0  # type: int

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
        self.alive_players = []
        self.coins = []
        self.connections = []
        self.npcs_left = 20
        self.time_left = 300
        self.ticks = 0

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
        self.alive_players = self.players[:]  # copy list

    def set_drawer(self):
        self.drawer = Drawer(self)
        self.drawer.bake_static_background()

    def set_next_player(self, connection):
        self.connections.append(connection)
        for player in self.players:
            if player.ready:
                continue
            player.set_connection(connection)
            return player 
        else:
            return None

    def is_ready(self):
        return all(player.ready for player in self.players)

    def is_over(self):
        return (
            self.time_left <= 0
            or len(self.alive_players) < 2
            or len(self.npcs) + self.npcs_left == 0
        )

    def get_monsters_chain(self):
        return chain(
            self.alive_players,
            self.npcs,
            self.bullets,
        )

    def get_all_chain(self):
        return chain(
            self.alive_players,
            self.npcs,
            self.bullets,
            self.walls,
        )

    def get_tanks_chain(self):
        return chain(self.alive_players, self.npcs)

    async def broadcast(self, data):
        events = [
            connection.write(data)
            for connection in self.connections
        ]
        if events:
            await wait(events)

    async def send_informations(self):
        for monster in self.get_monsters_chain():
            data = messages.get_monster_serialized_move_data(monster)
            await self.broadcast(data)

    async def step(self):
        if self.is_ready() and not self.is_over():
            await self.logic.step()
            await self.send_informations()
        if self.drawer is not None:
            self.drawer.render()
