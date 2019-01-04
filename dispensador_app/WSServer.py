#!/usr/bin/env python
import asyncio
import websockets
from crontab import CronTab
from datetime import datetime, date

cron = CronTab(user='m')

def crear_trabajo(cron, date, hour, gramos):
    date = date.strip("/").split()
    hour = date.strip(":").split()
    job  = cron.new(command='python Servo_Motor.py '+ gramos)
    job.setall(datetime(int(str(date.today().year)), date[0], date[1], hour[0], hour[1]))
    job.enable()
    cron.write_to_user(user="m")

def eliminar_trabajos_pasados(cron):
    for job in cron:
        day,month= "",""
        if(int(str(job[2]))<10):
            day="0"+str(job[2])
        if(int(str(job[3]))<10):
            month="0"+str(job[3])
        year=str(date.today().year)
        day,month,year=int(day),int(month),int(year)
        job_date2=date(year,month,day)
        print(date.today())
        if(job_date2 < date.today()):
            cron.remove(job)
            print("Trabajo Eliminado")
        else:
            print("Trabajo aún sin realizar")
        cron.write_to_user(user="m")

async def echo(websocket, path):
    async for message in websocket:
        print(message)
        mesagge=message.strip("_").split()
        crear_trabajo(cron, message[1], message[2], message[3])


start_server = websockets.serve(echo,"0.0.0.0" ,5678)
print("Inciando WSServer 192.168.0.31:5678")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
