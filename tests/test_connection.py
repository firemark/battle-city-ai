from battle_city.connection import PlayerConnection
from asynctest.mock import CoroutineMock, call

import pytest


@pytest.mark.asyncio
async def test_client_write_small_message():
    writer = CoroutineMock()
    writer.drain = CoroutineMock()
    connection = PlayerConnection(reader=None, writer=writer)
    await connection.write({'test': 'test'})

    assert writer.method_calls == [
        call.write(b'{"test": "test"}'),
        call.write(b'\n'),
        call.drain(),
    ]
