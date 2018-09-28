from asyncio import get_event_loop, open_connection, ensure_future
from collections import defaultdict

import pygame
import json

COLORS = defaultdict(lambda: (0xff, 0xff, 0xff),
    player=(0xff, 0xff, 0x00),
    player2=(0x00, 0xff, 0x00),
    npc=(0x88, 0x88, 0x88),
    tinywall=(0x88, 0x00, 0x00),
    metal=(0x33, 0x33, 0x33),
    water=(0x00, 0x00, 0xff),
    bullet=(0x88, 0x88, 0x88),
)

SIZES = defaultdict(lambda: 32,
    tinywall=8,
    bullet=4,
)


class Game(object):

    def __init__(self, loop, reader, writer):
        self.loop = loop
        self.reader = reader
        self.writer = writer
        self.map = {}
        self.player_id = None
        self.first_tick = False
        self.npc = 0
        self.time = 0
        self.draw = Draw(self)
        self.start = False
        self.end = False

        loop.call_soon(self._loop)

    async def loop_game(self):
        if not self.first_tick:
            await self.send(dict(action='greet', name='WINDOW'))
            self.first_tick = True

        self.draw.map()
        seconds_to_wait = 0.25
        loop.call_later(seconds_to_wait, self._loop)

    async def receive(self, data):
        if 'cords' in data:
            self.player_id = data['id']
            for cord in data['cords']:
                self._add_to_map(cord)
        elif data.get('status') == 'game':
            action = data['action']
            if action == 'info':
                self.time = data['ticks_left']
                self.npc = data['npcs_left']
            elif action == 'start':
                self.start = True
            elif action == 'over':
                self.end = True
        elif data.get('status') == 'data':
            id = data['id']
            if data['action'] in {'move', 'change', 'freeze'}:
                obj = self.map.get(id)
                if not obj:
                    return
                rect = obj['rect']
                rect.x = data['position']['x']
                rect.y = data['position']['y']
            elif data['action'] == 'destroy':
                self.map.pop(id, None)
            elif data['action'] == 'spawn':
                self._add_to_map(data)

    def _add_to_map(self, data):
        obj = dict()
        id = data['id']
        type = data['type']
        size = SIZES[type]
        if type == 'player' and id != self.player_id:
            color = COLORS['player2']
        else:
            color = COLORS[type]
        obj['rect'] = pygame.Rect(
            data['position']['x'],
            data['position']['y'],
            size,
            size,
        )
        obj['color'] = color

        self.map[data['id']] = obj

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


class Draw:

    def __init__(self, game):
        pygame.init()
        pygame.display.set_caption('WINDOW TEST CLIENT')
        self.game = game
        self.window = pygame.display.set_mode((512, 512 + 50), 0, 32)
        self.font = pygame.font.SysFont('monospace', 18, bold=True)

    def map(self):
        game = self.game
        self.window.fill((0, 0, 0))
        for obj in game.map.values():
            pygame.draw.rect(self.window, obj['color'], obj['rect'])

        label = 'NPC: {:03d} TIME: {:03d} {} {}'.format(
            game.npc,
            game.time,
            'START' if game.start else 'WAIT',
            'OVER' if game.end else '',
        )
        image = self.font.render(label, 1, (0xff, 0xff, 0xff))
        self.window.blit(image, (0, 512))
        pygame.display.update()


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
