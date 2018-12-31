#!/usr/bin/env python

import asyncio
import websockets
import schedule
import time
import datetime
import pigpio
from aiofile import AIOFile, LineReader, Writer


servo_motor=pigpio.pi()

def activar_dispensador(gramos,id):
    servo=23
    print(servo)
    angulo_abierto=int(150*11.111)+500 #150 es el angulo variable
    angulo_cerrado=int(10*11.111)+500 #10 es el angulo variable
    if angulo > 2500:
        angulo=2500
    elif angulo < 500:
        angulo=500
    servo_motor.set_servo_pulsewidth(servo,angulo_abierto)
    time.sleep(gramos)
    servo_motor.set_servo_pulsewidth(servo,angulo_cerrado)
    return schedule.CancelJob

async def borrar_tarea(id):
    lines = []
    async with AIOFile("tareas.txt", 'r') as afp:
        async for line in LineReader(afp):
            lines.append(line)
    async with AIOFile("tareas.txt", 'w') as afp:
        async for linea in lines:
            if linea.strip("_").split()[0] != id:
                writer = Writer(afp)
                await writer(line+"\n")
        await afp.fsync()

actual = datetime.day +"-"+ datetime.month +"-"+ datetime.year

#Mensaje: ID_IP_DIA_HORA_GR
async def programar_trabajos(gramos):
    async with AIOFile("tareas.txt", 'r') as afp:
        async for line in LineReader(afp):
            schedule.every().day.at(line.strip("_").split[3]).do(activar_dispensador,gramos,line.strip("_").split()[0])



async def echo(websocket, path):
    numero=0
    #Manejo de Mensaje (Nueva conexión, Nuevo horario o reseteo de horario)
    async with AIOFile("tareas.txt", 'r') as afp:
        async for line in LineReader(afp):
            print(line)
            await websocket.send(line)
            numero=line.strip("_").split()[0]
    async for message in websocket:
        async with AIOFile("tareas.txt", 'a+') as afp:
            await afp.write(str(numero)+"_"+message+"\n")
            await websocket.send(message)
            activar_dispensador(2)


shedule.run_continuously()
start_server = websockets.serve(echo,"0.0.0.0" ,5678)
print("Inciando WSServer 192.168.0.31:5678")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
