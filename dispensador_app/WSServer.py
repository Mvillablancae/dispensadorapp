#!/usr/bin/env python

import asyncio
import websockets
import schedule
import time
import pigpio
from aiofile import AIOFile, LineReader, Writer


servo_motor=pigpio.pi()

def move_servo(movimiento):
    servo=23
    print(servo)
    angulo=int(movimiento.split("_")[1])
    angulo=int(angulo*11.111)+500
    if angulo > 2500:
        angulo=2500
    elif angulo < 500:
        angulo=500
    delay_period=0.01
    print ("Moviendo Servo "+str(servo)+", "+str(angulo)+"grados.")
    time.sleep(1)
    servo_motor.set_servo_pulsewidth(servo,angulo)


async def echo(websocket, path):
    #Manejo de Mensaje (Nueva conexión, Nuevo horario o reseteo de horario)
    async with AIOFile("tareas.txt", 'r') as afp:
        async for line in LineReader(afp):
            print(line)
            await websocket.send(line)
    async for message in websocket:
        async with AIOFile("tareas.txt", 'a+') as afp:
            await afp.write(message)
            await websocket.send(message)
            move_servo("m1_50")

start_server = websockets.serve(echo,"0.0.0.0" ,5678)
print("Inciando WSServer 192.168.0.31:5678")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
