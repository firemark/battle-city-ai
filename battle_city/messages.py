def get_monster_serialized_data(monster, action='change'):
    return dict(
        status='data',
        action=action,
        id=monster.id.hex,
        type=monster.get_type(),
        speed=monster.speed,
        position=monster.get_position(),
        is_freeze=monster.is_freeze,
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
