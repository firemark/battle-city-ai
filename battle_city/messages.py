def get_monster_serialized_data(monster, action='change'):
    return dict(
        status='data',
        action=action,
        id=monster.id.hex,
        type=monster.get_type(),
        speed=monster.speed,
        position=monster.get_position(),
        is_freeze=monster.is_freeze,
        parent=monster.parent and monster.parent.id.hex,
        direction=monster.direction.value,
    )


def get_monster_serialized_move_data(monster):
    return dict(
        status='data',
        action='move',
        id=monster.id.hex,
        position=monster.get_position(),
    )


def get_basic_data(monster):
    return dict(
        type=monster.get_type(),
        id=monster.id.hex,
        position=monster.get_position(),
    )


def get_world_data(player, game):
    return dict(
        id=player.id.hex,
        cords=[get_basic_data(monster) for monster in game.get_all_chain()]
    )


def get_start_game_data():
    return dict(
        status='game',
        action='start',
    )


def get_over_game_data(game):
    players = sorted(game.alive_players, key=lambda player: -player.score)
    try:
        player = players[0]
    except KeyError:
        return dict(
            status='game',
            action='over',
            winner=None,
        )

    return dict(
        status='game',
        action='over',
        winner=player.id.hex,
    )


def get_tick_game_data(game):
    return dict(
        status='game',
        action='info',
        ticks_left=game.time_left,
        npcs_left=len(game.npcs),
    )
