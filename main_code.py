#!/usr/bin/env python3
# Note: DC means that line is temporary Debug Code
#Imports
from ev3dev2.display import Display
from ev3dev2.display import fonts
myfont=fonts.load('lutBS18')
show=Display()
from ev3dev2.button import Button 
from ev3dev2 import list_devices
from ev3dev2.port import LegoPort
from ev3dev2.motor import (Motor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, OUTPUT_C,
                            MoveDifferential, SpeedRPM)
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, TouchSensor
from ev3dev2.sensor import INPUT_1,INPUT_2, INPUT_3, INPUT_4
import random
import math
import time
from ev3dev2.wheel import EV3EducationSetTire
import paho.mqtt.client as mqtt

initiator=0
client = mqtt.Client()
broker_address="192.168.7.212"
client.connect(broker_address)
recieved=0
def on_message(client, userdata, message):
    str(message.payload.decode("utf-8"))
    global recieved
    recieved=int(message.payload.decode("utf-8"))
    print(recieved)
#Address of EV3 broker
#Create a client that will recieve messages
client=mqtt.Client()
#Set on_message funcion of client to my on_message function
client.on_message=on_message
#Connects to ev3 broker
client.connect(broker_address)
#Subscribe to channel
client.subscribe('snoofer_bot_reception')
#Starts loop to handle callbacks
client.loop_start()
# This is the Publisher
client = mqtt.Client()
client.connect("192.168.7.212")

#Function defines

def get_snoofer_angle(motorpos):
    angle=-19.03*math.cos(math.radians(motorpos)-0.0123)-1.9
    return angle

##def zero_in():
 #   move.on(15,15)
 #   while sensor.distance_centimeters>4:
 #       if left_whisker.is_pressed==True:
  #          move.off()
  #          move.on_for_distance(27, -20, brake=True, block=True)
  #          move.turn_degrees(30, -20)
  #          move.on(15,15)
  #      if right_whisker.is_pressed==True:
  #          move.off()
  #          move.on_for_distance(27, -20, brake=True, block=True)
   #         move.turn_degrees(30, 20)
   #         move.on(15,15)

def turn():
    turn_angle=10*random.randrange(4,19)
    turn_direction_decider=random.randrange(1,3)
    if turn_direction_decider==1:
        turn_direction=-1
    if turn_direction_decider==2:
        turn_direction=1
    final_turn=turn_angle*turn_direction
    #leftmotor.position=0
    #rightmotor.position=0
    return final_turn

def telemetry(robot_x,robot_y,s_ang,s_dist):
    object_x=math.cos(s_ang)*(s_dist)
    object_y=math.sin(s_ang)*(s_dist)
    f.write(str("\n Relative coordinates:"))
    f.write(str(object_x) + '\n')
    f.write(str(object_y) + '\n')
    object_x+=robot_x
    object_y+=robot_y
    return object_x, object_y

def send_coords(string,broker_adress):
    client.publish("snoofer_bot_transmission",string)


def load_sensor(port,mode,device): 
    #Function to initiate sensors; port should be INPUT_N where N is 1 to 4
    #mode is a string describing which driver to use (see https://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/sensors.html#supported-sensors)
    #device is also a string, see site above
    sensor=LegoPort(port)
    sensor.mode=mode
    if device=='lego-ev3-gyro':
        sensor.set_device=device
    time.sleep(0.5)
    return sensor


f = open('inputfile', 'w')

show.text_pixels("Use side buttons to \n move snoofer so \n orange pointer is \n over orange peg \n press mid button \n when done", x=10, y=10, font=fonts.load('lutBS14'))
show.update()
button=Button()
snoofermotor=Motor(OUTPUT_A)
sensorport=load_sensor(port='pistorms:BBS1', mode='ev3-uart', device='lego-ev3-us')
time.sleep(0.5)
sensor=UltrasonicSensor('pistorms:BBS1')
#The following must be redone once some sort of viable input is established
while initiator==0:
    time.sleep(0.1)
    if button.enter:
        snoofermotor.run_forever(speed_sp=101)
    if button.enter==False:
        snoofermotor.stop()
    if sensor.distance_centimeters<5:
        initiator=1
    
        
#Drive syntax
#Give sensor drivers 1 second each to load
initiator=1
if initiator==1:
    show.clear()
    pre_terminate=0 #DC
    random.seed(12)
    show.update()
    object_found=0
    bot_x=0
    bot_y=0
    snoofermotor.position=0
    gyroport=load_sensor(port='pistorms:BAS1', mode='ev3-uart',device='lego-ev3-gyro')
    gyro=GyroSensor('pistorms:BAS1')
    move=MoveDifferential(OUTPUT_C, OUTPUT_D, EV3EducationSetTire, 152)
    leftmotor=Motor(OUTPUT_C)
    rightmotor=Motor(OUTPUT_A)
    terminate=0
    move.odometry_start()
    move.gyro=gyro
    #noise=Sound()
    gyro.calibrate()
    time.sleep(1)
    while terminate==0:
        move.on(40,40)
        snoofermotor.run_forever(speed_sp=360)
        distance=sensor.distance_centimeters
        if button.enter:
            snoofermotor.stop()
            p=get_snoofer_angle(snoofermotor.position%360)
            print (snoofermotor.position%360)
            print(p)
            time.sleep(12)
        #if sensor.distance_centimeters<36:
       #     snoofermotor.stop()
      #      snoofermotor.position=snoofermotor.position%360
      #      snoofermotor.run_to_abs_pos(position_sp=70,speed_sp=360)
            #zero_in()
      #      object_found=1
      # 
      # elif left_whisker.is_pressed==True:
        #    snoofermotor.stop()
       #     move.off()
      #      snoofermotor.position=snoofermotor.position%360
       #     snoofermotor.run_to_abs_pos(position_sp=70,speed_sp=360)
      #      move.on_for_distance(27, 20, brake=True, block=True)
      #      zero_in()
      #      object_found=1
           
      #  elif right_whisker.is_pressed==True:
      #      snoofermotor.stop()
      #      move.off()
      #      snoofermotor.position=snoofermotor.position%360
      #      snoofermotor.run_to_abs_pos(position_sp=70,speed_sp=360)
      #      move.on_for_distance(27, -20, brake=True, block=True)
      #      zero_in()
      #      object_found=1
     #
      #  else: 
      #      pass
        if object_found==1:
            move.off()
            snoofer_ang=math.radians(get_snoofer_angle(snoofermotor.position))
            gyro_angle=math.radians(-gyro.angle+90)
            snoofer_ang_final=snoofer_ang+gyro_angle
            snooferdistance=(sensor.distance_centimeters*10)+85
            bot_x=move.x_pos_mm
            bot_y=move.y_pos_mm
            object_x,object_y=telemetry(bot_x,bot_y,snoofer_ang_final,snooferdistance)
            #noise.beep()
            object_x_str=str(math.trunc(object_x))
            object_y_str=str(math.trunc(object_y))
            coord_str=object_x_str + ',  ' + object_y_str
            send_coords(coord_str,broker_address)
            f.write(str('Bot Position:'))
            f.write(str(bot_x) + '\n')
            f.write(str(bot_y) + '\n')
            #f.write(str(temp)+ '\n')
            #f.write(str(leftmotor.count_per_rot))
            # f.write('Relative snoofer angle: '+'\n')
            #f.write(str(snoofer_ang)+'\n')
            f.write('Gyro angle:'+'\n')
            f.write(str(gyro_angle)+'\n')
            # f.write ("Absolute snoofer angle: "+'\n')
            # f.write (str(snoofer_ang_final) + '\n')
            #f.write ('Snoofer distance:'+'\n')
            # f.write (str(snooferdistance) + '\n')
            #f.write ("Object coordinates:"+'\n')
            # f.write (coord_str)
            
            random.seed(math.trunc(snooferdistance*move.x_pos_mm+gyro_angle))
            show.update()
            time.sleep(0.5)
            move.on_for_distance(27, -100, brake=True, block=True)
            move.turn_degrees(31,turn())
            object_found=0
            pre_terminate+=1
            if pre_terminate==24:
                terminate=1



abort_str=str(440440440440) + ',  ' + str(440440440440)
send_coords(abort_str,broker_address)
time.sleep(1)
temp=str(gyro.angle)
f.write(temp)
f.close()