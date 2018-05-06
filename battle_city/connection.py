from asyncio import StreamWriter, StreamReader

import json


class PlayerConnection(object):
    writer: StreamWriter
    reader: StreamReader
    buffer: bytes = b''

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.writer = writer
        self.reader = reader

    async def read(self):
        buffer = await self.reader.readline()
        try:
            return json.loads(buffer)
        except json.JSONDecodeError:
            return None 

    async def write(self, data):
        writer = self.writer
        raw_data = json.dumps(data).encode()
        writer.write(raw_data)
        writer.write(b'\n')
        await writer.drain()

    async def write_ok(self, **kwargs):
        data = {'status': 'OK'}
        data.update(kwargs)
        await self.write(data)

    async def write_error(self, message):
        await self.write({'status': 'ERROR', 'message': message})
