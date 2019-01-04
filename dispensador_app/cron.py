from crontab import CronTab
from datetime import datetime, date

cron = CronTab(user='m')


def crear_trabajo(cron, date, hour, gramos):
    date=date.strip("/").split()
    hour=date.strip(":").split()
    job  = cron.new(command='python archivos.py '+gramos)
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