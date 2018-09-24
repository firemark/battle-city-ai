from battle_city.connection import PlayerConnection
from battle_city.game import Game
from battle_city.monsters import Player

from asynctest.mock import patch, CoroutineMock

patch_messages = patch('battle_city.action_handler.messages')


def make_player(had_action=False, x=1, y=2):
    player = Player(x=x, y=y, player_id=0)
    player.had_action = had_action
    connection = PlayerConnection(None, None)
    connection.write = CoroutineMock(spec=connection.write)
    player.set_connection(connection)

    return player


def make_game(*players):
    game = Game()
    game.alive_players = players

    return game
