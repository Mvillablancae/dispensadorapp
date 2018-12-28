#!/usr/bin/env python

import asyncio
import websockets
from aiofile import AIOFile, LineReader, Writer

async def echo(websocket, path):
    #Manejo de Mensaje (Nueva conexión, Nuevo horario o reseteo de horario)
    async with AIOFile("tareas.txt", 'r') as afp:
        async for line in LineReader(afp):
            print(line)
            await websocket.send(line)
    async for message in websocket:
        async with AIOFile("tareas.txt", 'a+') as afp:
            await afp.write(message)


start_server = websockets.serve(echo, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
