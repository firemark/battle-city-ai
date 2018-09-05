from battle_city.game import Game
from battle_city.basic import Direction
from battle_city.monsters import Player

from battle_city import messages


class ActionHandler(object):

    @staticmethod
    async def write_ok(player: Player, **data):
        await player.connection.write_ok(**data)

    @staticmethod
    async def write_error(player: Player, error: str):
        await player.connection.write_error(error)

    @classmethod
    async def can_has_action(cls, game: Game, player: Player):
        if player.had_action:
            await cls.write_error(player, 'too many actions per turn')
            return False
        else:
            await cls.set_had_action(player, game)
            return True

    @classmethod
    async def action_undefined(cls, data: dict, player: Player, game: Game):
        await cls.write_error(player, 'unknown action')

    @classmethod
    async def action_rotate(cls, data: dict, player: Player, game: Game):
        raw_direction: str = data.get('direction', '').lower()
        try:
            direction = Direction(raw_direction)
        except ValueError:
            await cls.write_error(player, 'unknown direction')
            return

        with await game.step_lock:
            if not await cls.can_has_action(game, player):
                return
            player.set_direction(direction)
            await cls.set_had_action(player, game)
        await cls.write_ok(player, direction=direction.value)

    @classmethod
    async def action_set_speed(cls, data: dict, player: Player, game: Game):
        speed = data.get('speed')
        if not isinstance(speed, int):
            await cls.write_error(player, 'speed has wrong value')
            return

        with await game.step_lock:
            if not await cls.can_has_action(game, player):
                return
            player.set_speed(speed)
            await cls.set_had_action(player, game)
        await cls.write_ok(player, speed=speed)

    @classmethod
    async def action_shot(cls, data: dict, player: Player, game: Game):
        with await game.step_lock:
            if not await cls.can_has_action(game, player):
                return
            player.set_shot()
            await cls.set_had_action(player, game)
        await cls.write_ok(player) 

    @staticmethod
    async def set_had_action(player: Player, game: Game):
        player.set_had_action()
        data = messages.get_monster_serialized_data(player)
        await game.broadcast(data)

