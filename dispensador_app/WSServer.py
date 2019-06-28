#!/usr/bin/env python
import asyncio
import websockets
from crontab import CronTab
from datetime import datetime, date
import os
import sys

cron = CronTab(user='m')
nivel_critico=10000
ultimo_id=0

def agregar_linea(date_j,hour,gramos):
    arch=open("id_tareas.txt","a+")
    global ultimo_id
    ultimo_id+=1
    linea=str(ultimo_id)+"_"+date_j+"_"+hour+"_"+gramos+'\n'
    arch.write(linea)

def actualizar_id():
    global ultimo_id
    with open("id_tareas.txt","r") as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        print(last_line)
        ultimo_id=int(last_line.strip().split("_")[0])


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
        print(job_date2)
        if(job_date2 < date.today()):
            cron.remove(job)
            print("Trabajo Eliminado")
        else:
            print("Trabajo aun sin realizar")
        cron.write_to_user(user="m")

def eliminar_trabajo(cron, date_j, hour, gramos):
    for job in cron:
        dia,mes=date_j.strip().split("/")
        minuto,hora=hour.strip().split(":")
        if int(minuto)==job[0] and int(hora)==job[1] and int(dia)==job[2] and int(mes)==job[3] and int(gramos)==job[7]:
            cron.remove(job)
            print("Trabajo Eliminado")
        cron.write_to_user(user="m")

def actualizar_trabajo(cron, date_j, hour, gramos, prevWork):
    date_j = date_j.strip().split("/")
    hour = hour.strip().split(":")
    print(date_j,hour)
    Motor_command="/home/pi/Servo_Motor.py "+gramos
    job  = cron.new(command='/home/pi/.local/bin/python3 '+Motor_command)
    job.setall(datetime(int(str(date.today().year)), int(date_j[1]), int(date_j[0]), int(hour[0]), int(hour[1])))
    job.enable()
    cron.write_to_user(user="m")
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
        cron.write_to_user(user="m")
        print(date_j,hour)
    

async def echo(websocket, path):
    async for message in websocket:
        message=str(message).strip().split("_")
        print(message)
        await websocket.send(str(ultimo_id)+'_'+message[1]+'_'+message[2]+'_'+message[3])
        agregar_linea(message[1],message[2],message[3])
        if message[0] == "Nivel":
            nivel_critico=int(str(message).strip().split("_")[1])
            print(message[0])
        elif message[0] == "Agregar":
            crear_trabajo(cron, message[1], message[2], message[3])
            print(message[0])
        elif message[0] == "Eliminar":
            eliminar_trabajo(cron, message[1], message[2], message[3])
            print(message[0])
        elif message[0] == "Actualizar":
            actualizar_trabajo(cron, message[1], message[2], message[3])
            print(message[0])
        print("--------------- FOR -----------")
        for job in cron:
            print(job)

start_server = websockets.serve(echo,"0.0.0.0" ,5678)
print("Inciando WSServer localhost:5678")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()