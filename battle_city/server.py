from asyncio import sleep, start_server, wait, get_event_loop
from battle_city.game import Game
from battle_city.action_handler import ActionHandler
from battle_city.connection import PlayerConnection

from argparse import ArgumentParser

parser = ArgumentParser(description='Server of battle city')
parser.add_argument(
    '--ip', type=str, help='ip of server to listen', default='127.0.0.1')
parser.add_argument(
    '--port', type=int, help='port of server to listen', default=8888)
parser.add_argument(
    '--map', type=str, help='path to map', default='pilif')
parser.add_argument('--hidden-window', action='store_true', default=False)
parser.add_argument('--speed', type=float, default=1, help='tick speed in milliseconds')


async def game_loop(game: Game, speed: float=0.033):
    while True:
        await wait([
            game.step(),
            sleep(speed),
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
        try:
            data = await connection.read()
        except ConnectionError:
            return
        if data is None:
            continue
        await handle_action(data, player, game)
       

async def handle_action(data: dict, player, game):
    action = 'action_' + data.get('action', 'undefined')
    action_undefined = ActionHandler.action_undefined
    method = getattr(ActionHandler, action, action_undefined)
    await method(data=data, player=player, game=game)


def run():
    args = parser.parse_args()

    game = Game()
    game.load_map(args.map)
    if not args.hidden_window:
        game.set_drawer()
    loop = get_event_loop()
    coro_server = start_server(
        handle_connection(game), args.ip, args.port,
        loop=loop,
    )

    server = loop.run_until_complete(coro_server)
    loop.run_until_complete(game_loop(game, 33 / args.speed / 1000))

    try:
        loop.run_forever()
    except EOFError:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run()
