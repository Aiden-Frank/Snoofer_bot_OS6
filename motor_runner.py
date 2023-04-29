#!/usr/bin/env python3
from ev3dev2.motor import (Motor, MediumMotor, OUTPUT_A, SpeedRPM)
from ev3dev2.display import fonts
from ev3dev2.display import Display
myfont=fonts.load('lutBS18')
show=Display()
snoofermotor=Motor(OUTPUT_A)

while True:
    command=input('F for one way, G for other')
    if command=='f':
        snoofermotor.run_forever(speed_sp=360)
    elif command=='g':
        snoofermotor.run_forever(speed_sp=-360)
    elif command=='v':
        snoofermotor.run_forever(speed_sp=100)
    elif command=='b':
        snoofermotor.run_forever(speed_sp=-100)
    elif command=='zero':
        snoofermotor.position=0
    else:
        snoofermotor.stop()
    p=snoofermotor.position
    while p>359:
        p-=360
    while p<0:
        p+=360
    print(p)
    