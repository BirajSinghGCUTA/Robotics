#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor, UltrasonicSensor, TouchSensor)
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait

EV3_DETECT = 15
NXT_DETECT = 40

TURN_TIME_90 = 1250
TURN_TIME_180 = 2500
TURN_SPEED_180 = 125

ev3 = EV3Brick()

# Initialize Sensors & Motors
col_sensor = ColorSensor(Port.S1)
l_touch = TouchSensor(Port.S2)
r_touch = TouchSensor(Port.S3)
eyes = UltrasonicSensor(Port.S4)

l_touchBtn = "Off"
r_touchBtn = "Off"

left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

ev3.speaker.say("Starting program")
theVal = 0
theTime = 0

while True:
    if theVal != 100:
        theVal += 1

    if theTime != 50:
        theTime += 1
    
    if theVal == 100 and theTime == 50:
        theTime = 0
        theVal0 = 0
    
    while r_touch.pressed() is False and l_touch.pressed() is False:
        print(eyes.distance())
        if eyes.distance() > 100:
            left_motor.run(-200)
            right_motor.run(-100 - theVal)
        else:
            left_motor.run(-200)
            right_motor.run(-200)
            

    if r_touch.pressed() is True or l_touch.pressed() is True:
        left_motor.run_time(100, 1000, wait = False)
        right_motor.run_time(300, 1000)

    wait(10)

ev3.speaker.say("Goal found")

