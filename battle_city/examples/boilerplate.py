from asyncio import get_event_loop, open_connection, ensure_future

import json


class Game(object):

    def __init__(self, loop, reader, writer):
        self.loop = loop
        self.reader = reader
        self.writer = writer
        self.first_tick = False

        loop.call_soon(self._loop)

    async def loop_game(self):
        """
        sometimes execute any random action
        """
        if not self.first_tick:
            await self.send(dict(action='greet', name='TEST'))
            self.first_tick = True

        # await self.send(json_data)
        seconds_to_wait = 0.25
        loop.call_later(seconds_to_wait, self._loop)

    async def receive(self, data):
        """
        get json from server and do something
        for example show on console data
        """
        pass

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
