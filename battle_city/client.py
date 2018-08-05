from asyncio import get_event_loop, open_connection, ensure_future
from random import randint, choice

from functools import partial

import json


async def handle_client(loop):
    reader, writer = await open_connection('127.0.0.1', 8888, loop=loop)
    print('CONNECTED!')

    loop.call_soon(change_state_callback, loop, writer)

    while True:
        raw_data = await reader.readline()
        data = json.loads(raw_data)
        print(data)


def change_state_callback(loop, writer):
    # wtf? py3 why?
    ensure_future(change_state(loop, writer))


async def change_state(loop, writer):
    action = randint(0, 2)

    if action == 0:
        speed = randint(0, 2)
        data = dict(action='set_speed', speed=speed)
    elif action == 1:
        direction = choice(['up', 'down', 'left', 'right'])
        data = dict(action='rotate', direction=direction)
    else:
        data = dict(action='shot')

    if data is not None:
        data = json.dumps(data)
        writer.write(data.encode())
        writer.write(b'\n')
        await writer.drain()

    t = randint(1, 4) * 0.25
    loop.call_later(t, change_state_callback, loop, writer)


loop = get_event_loop()
handler = handle_client(loop)
loop.run_until_complete(handler)
loop.close()
