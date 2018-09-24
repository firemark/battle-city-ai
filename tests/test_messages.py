from battle_city.basic import Direction
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


def test_messages_get_move_data():
    player = Player(x=1, y=2, player_id=0)

    assert messages.get_monster_serialized_move_data(player) == dict(
        id=player.id.hex,
        status='data',
        action='move',
        position={'x': 1, 'y': 2},
    )


def test_messages_get_monster_data():
    player = Player(x=1, y=2, player_id=0)
    player.direction = Direction.UP
    player.speed = 2

    assert messages.get_monster_serialized_data(player, action='socek') == dict(
        id=player.id.hex,
        type='player',
        status='data',
        action='socek',
        is_freeze=False,
        direction='up',
        speed=2,
        parent=None,
        position={'x': 1, 'y': 2},
    )


def test_messages_get_bullet_data():
    player = Player(x=1, y=2, player_id=0)
    bullet = Bullet(x=1, y=2)
    bullet.set_direction(direction=Direction.UP)
    bullet.set_parent(player)

    assert messages.get_monster_serialized_data(bullet, action='socek') == dict(
        id=bullet.id.hex,
        type='bullet',
        status='data',
        action='socek',
        is_freeze=False,
        direction='up',
        speed=8,
        parent=player.id.hex,
        position={'x': 1, 'y': 2},
    )


def test_messages_get_start_game_data():
    assert messages.get_start_game_data() == dict(
        status='game',
        action='start',
    )


def test_messages_get_over_game_data():
    player_a = Player(x=1, y=2, player_id=0)
    player_b = Player(x=1, y=2, player_id=1)
    player_a.score = 20
    player_b.score = 40
    game = Game()
    game.alive_players = [player_a, player_b]

    assert messages.get_over_game_data(game) == dict(
        status='game',
        action='over',
        winner=player_b.id.hex,
    )


def test_messages_get_tick_game_data():
    game = Game()
    game.time_left = 42
    game.npcs = [object(), object()]

    assert messages.get_tick_game_data(game) == dict(
        status='game',
        action='info',
        ticks_left=42,
        npcs_left=2,
    )
