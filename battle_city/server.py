from asyncio import sleep, start_server, wait, get_event_loop
from battle_city.game import Game
from battle_city.action_handler import ActionHandler
from battle_city.connection import PlayerConnection

import json


async def game_loop(game: Game):
    while True:
        await wait([
            game.step(),
            sleep(0.033),
        ])


def handle_connection(game):

    async def callback(reader, writer):
        connection = PlayerConnection(reader, writer)
        player = game.set_next_player(connection)
        if player is not None:
            await handle_actions(connection, player=player, game=game)

        writer.close()

    return callback


async def handle_actions(connection, player, game):
    while True:
        data = await connection.read()
        await handle_action(connection, data, player, game)
       

async def handle_action(connection, data: dict, player, game):
    action = 'action_' + data.get('action', 'undefined')
    action_undefined = ActionHandler.action_undefined
    method = getattr(ActionHandler, action, action_undefined)
    await method(data=data, player=player, game=game)


def run():
    game = Game()
    loop = get_event_loop()
    coro_server = start_server(
        handle_connection(game), '0.0.0.0', 8888,
        loop=loop,
    )

    server = loop.run_until_complete(coro_server)
    loop.run_until_complete(game_loop(game))

    try:
        loop.run_forever()
    except EOFError:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run()
