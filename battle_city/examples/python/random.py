from asyncio import get_event_loop, open_connection, ensure_future
from random import randint, choice

import json
import sys

try:
    is_silent = sys.argv[1] == 'silent'
except IndexError:
    is_silent = False


class Game(object):

    def __init__(self, loop, reader, writer):
        self.loop = loop
        self.reader = reader
        self.writer = writer
        self.first_tick = False
        self.start = False

        loop.call_soon(self._loop)

    async def loop_game(self):
        """
        sometimes execute any random action
        for example this tank make random choices (is a dummy tank!)
        """
        if not self.first_tick:
            await self.send(dict(action='greet', name='TEST'))
            self.first_tick = True

        if self.start:
            action = randint(0, 2)

            if action == 0:
                speed = randint(0, 2)
                data = dict(action='set_speed', speed=speed)
            elif action == 1:
                direction = choice(['up', 'down', 'left', 'right'])
                data = dict(action='rotate', direction=direction)
            else:
                data = dict(action='shoot')

            await self.send(data)

        seconds_to_wait = 0.25
        loop.call_later(seconds_to_wait, self._loop)

    async def receive(self, data):
        """
        get json from server and do something
        for example show on console data
        """

        if data.get('action') == 'move':
            return  # too many data ;_;

        if data.get('status') == 'ERROR':
            color = '\033[91m'  # red color
        elif data.get('status') == 'game':
            color = '\033[34m'  # blue color
            if data.get('action') == 'start':
                self.start = True
            elif data.get('action') == 'over':
                self.start = False
        elif data.get('action') == 'spawn':
            color = '\033[92m'  # green color
        elif data.get('action') == 'destroy':
            color = '\033[93m'  # orange color
        else:
            color = '\033[0m'  # default color

        if is_silent:
            return

        print(color, data, '\033[0m')

    async def send(self, data):
        if data is None:
            return
        raw_data = json.dumps(data)
        writer = self.writer
        writer.write(raw_data.encode())
        writer.write(b'\n')
        await writer.drain()

    def _loop(self):
        return ensure_future(self.loop_game())


async def handle_client(loop):
    reader, writer = await open_connection('127.0.0.1', 8888, loop=loop, limit=256 * 1000)
    print('\033[1mCONNECTED!\033[0m')

    game = Game(loop, reader, writer)

    while True:
        raw_data = await reader.readline()
        data = json.loads(raw_data)
        await game.receive(data)


if __name__ == "__main__":
    loop = get_event_loop()
    handler = handle_client(loop)
    loop.run_until_complete(handler)
    loop.close()
