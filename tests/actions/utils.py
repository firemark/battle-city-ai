from battle_city.connection import PlayerConnection
from battle_city.game import Game
from battle_city.monsters import Player

from asynctest.mock import CoroutineMock


def make_player():
    player = Player(x=1, y=2, player_id=0)
    connection = PlayerConnection(None, None)
    connection.write = CoroutineMock(spec=connection.write)
    player.set_connection(connection)

    return player


def make_game(*players):
    game = Game()
    game.alive_players = players

    return game
