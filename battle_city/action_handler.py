from battle_city.game import Game
from battle_city.basic import Direction
from battle_city.monsters import Player


class ActionHandler(object):

    @staticmethod
    async def action_undefined(data: dict, player: Player, game: Game):
        await player.connection.write_error('unknown action')

    @staticmethod
    async def action_rotate(data: dict, player: Player, game: Game):
        raw_direction: str = data.get('direction', '').lower()
        try:
            direction = Direction(raw_direction)
        except ValueError:
            await player.connection.write_error('unknown direction')
            return

        player.set_direction(direction)
        await player.connection.write_ok(direction=direction.value)

    @staticmethod
    async def action_set_speed(data: dict, player: Player, game: Game):
        speed = data.get('speed')
        if not isinstance(speed, int):
            await player.connection.write_error('speed has wrong value')
            return

        player.set_speed(speed)
        await player.connection.write_ok(speed=speed)

    @staticmethod
    async def action_shot(data: dict, player: Player, game: Game):
        player.is_shot = True
        await player.connection.write_ok()
        
