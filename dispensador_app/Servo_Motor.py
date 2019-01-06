import pigpio
import sys

import os
print('USER:'+os.environ['USER'])
print('PATH:'+os.environ['PATH'])
print('LOGNAME'+os.environ['LOGNAME'])
print('SHELL'+os.environ['SHELL'])

servo_motor=pigpio.pi()
def activar_dispensador(gramos):
    servo=23
    angulo_abierto=int(150*11.111)+500 #150 es el angulo variable
    angulo_cerrado=int(10*11.111)+500 #10 es el angulo variable
    if angulo > 2500:
        angulo=2500
    elif angulo < 500:
        angulo=500
    servo_motor.set_servo_pulsewidth(servo,angulo_abierto)
    time.sleep(gramos)
    servo_motor.set_servo_pulsewidth(servo,angulo_cerrado)

activar_dispensador(sys.argv[1])