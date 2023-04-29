#!/usr/bin/env python3
from ev3dev2.display import Display
from ev3dev2.sensor import INPUT_1,INPUT_2, INPUT_3, INPUT_4, Sensor
from ev3dev2.port import LegoPort
from ev3dev2.button import Button 
from smbus import SMBus
import time

stop=0

bus=SMBus(1)
def load_port(port,mode): 
    #Function to initiate sensors; port should be INPUT_N where N is 1 to 4
    #mode is a string describing which driver to use (see https://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/sensors.html#supported-sensors)
    #device is also a string, see site above
    port=LegoPort(port)
    port.mode=mode
    time.sleep(0.5)
    return port
left_whisker_port=load_port('pistorms:BBS2',"i2c-thru")
#right_whisker_port=load_port("pistorms:BAS2","i2c-thru")


left_whisker=Sensor('pistorms:BBS2')
#right_whisker=Sensor('pistorms:BAS2')

time.sleep(1)

while stop==0:
    right_value=right_whisker.value()
    print(right_value)
    time.sleep(0.5)
    if Button.enter==True:
        stop=1