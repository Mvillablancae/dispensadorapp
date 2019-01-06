#!/usr/bin/env python
import asyncio
import websockets
from crontab import CronTab
from datetime import datetime, date
import os
import sys

cron = CronTab(user='pi')

#cron.env['SHELL']='/bin/bash'
#cron.env['PATH']= '/home/pi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/gam$
#cron.env['LOGNAME']= 'pi'
#cron.env['USER']= 'pi'
#cron.env['HOME'] = '/home/pi'

#cron.write()


def crear_trabajo(cron, date_j, hour, gramos):
    print(date_j,hour)
    date_j = date_j.strip().split("/")
    hour = hour.strip().split(":")
    print(date_j,hour)
    Motor_command="/home/pi/Servo_Motor.py "+gramos
    job  = cron.new(command='/home/pi/.local/bin/python3 '+Motor_command)
    job.setall(datetime(int(str(date.today().year)), int(date_j[1]), int(date_j[0]), int(hour[0]), int(hour[1])))
    job.enable()
    cron.write_to_user(user="pi")

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
        print(job_date2)
        if(job_date2 < date.today()):
            cron.remove(job)
            print("Trabajo Eliminado")
        else:
            print("Trabajo aun sin realizar")
        cron.write_to_user(user="pi")

async def echo(websocket, path):
    async for message in websocket:
        print(message)
        message=str(message).strip().split("_")
        crear_trabajo(cron, message[1], message[2], message[3])
        for job in cron:
            print(job)

start_server = websockets.serve(echo,"0.0.0.0" ,5678)
print("Inciando WSServer 192.168.0.31:5678")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()