from random import randint, choice

import json



class Game(object):

    def __init__(self, loop, reader, writer):
        self.loop = loop
        self.reader = reader
        self.writer = writer
        self.first_tick = False
        self.start = False

    async def loop_game(self):
        """
        sometimes execute any random action
        for example this tank make random choices (is a dummy tank!)
        """
        if not self.first_tick:
            await self.send(action='greet', name='PYTHON')
            self.first_tick = True

        if self.start:
            action = randint(0, 2)

            if action == 0:  # set speed
                speed = randint(0, 2)
                await self.send(action='set_speed', speed=speed)
            elif action == 1:  # set direction
                direction = choice(['up', 'down', 'left', 'right'])
                await self.send(action='rotate', direction=direction)
            else:  # SHOT SHOT
                await self.send(action='shoot')

        self.call_soon(0.25)

    def call_soon(self, time):
        loop.call_later(time, self._loop)

    async def receive(self, data):
        """
        get json from server and do something
        for example show on console data
        """

        status = data.get('status')
        if status == 'data':
            if data.get('action') == 'move':
                return  # too many data ;_;
        elif status == 'game':
            action = data.get('action')
            if action == 'start':
                self.start = True
            elif action == 'over':
                self.start = False

        if is_silent:
            return

        print(self._get_color(data), data, '\033[0m')

    async def send(self, **data):
        if data is None:
            return
        raw_data = json.dumps(data)
        writer = self.writer
        writer.write(raw_data.encode())
        writer.write(b'\n')
        await writer.drain()

    def _loop(self):
        return ensure_future(self.loop_game())

    @staticmethod
    def _get_color(data):
        status = data.get('status')
        if status == 'ERROR':
            return '\033[91m'  # red color
        if status == 'OK':
            return '\033[35m'  # purple color
        if status == 'game':
            return '\033[34m'  # blue color
        if status == 'game':
            action = data.get('action')
            if action == 'spawn':
                return '\033[92m'  # green color
            if action == 'destroy':
                return '\033[93m'  # orange color
        return '\033[0m'  # default color


import sys

from asyncio import get_event_loop, open_connection, ensure_future

try:
    is_silent = sys.argv[1] == 'silent'
except IndexError:
    is_silent = False


async def handle_client(loop):
    reader, writer = await open_connection('127.0.0.1', 8888, loop=loop, limit=256 * 1000)
    print('\033[1mCONNECTED!\033[0m')

    game = Game(loop, reader, writer)
    loop.call_soon(game._loop)

    while True:
        raw_data = await reader.readline()
        data = json.loads(raw_data)
        await game.receive(data)


if __name__ == "__main__":
    loop = get_event_loop()
    handler = handle_client(loop)
    loop.run_until_complete(handler)
    loop.close()
