from battle_city.game import Game
from battle_city.monsters import Bullet, NPC, Player
from battle_city.monsters.wall import TinyWall, Water
from battle_city import messages


def test_messages_get_world_data():
    game = Game()

    player = Player(x=1, y=1, player_id=0)
    game.alive_players = [player]
    game.npcs = [NPC(2, 2)]
    game.bullets = [Bullet(3, 3)]
    game.walls = [TinyWall(x=4, y=4), Water(x=5, y=5)]

    assert messages.get_world_data(player, game) == dict(
        id=player.id.hex,
        cords=[
            dict(type='player', id=player.id.hex, position={'x': 1, 'y': 1}),
            dict(type='npc', id=game.npcs[0].id.hex, position={'x': 2, 'y': 2}),
            dict(type='bullet', id=game.bullets[0].id.hex, position={'x': 3, 'y': 3}),
            dict(type='tinywall', id=game.walls[0].id.hex, position={'x': 4, 'y': 4}),
            dict(type='water', id=game.walls[1].id.hex, position={'x': 5, 'y': 5}),
        ]
    )
