#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, ColorSensor, UltrasonicSensor, TouchSensor)
from pybricks.parameters import Port, Stop, Color, Direction
from pybricks.tools import wait

import random

ev3 = EV3Brick()

# Initialize Sensors & Motors
col_sensor = ColorSensor(Port.S1)
l_touch = TouchSensor(Port.S2)
r_touch = TouchSensor(Port.S3)
eyes = UltrasonicSensor(Port.S4)

l_touchBtn = "Off"
r_touchBtn = "Off"

left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)

ev3.speaker.say("Starting program")

theVal = 0
theTime = 0

wanderMode = False
followWallMode = False

# def followWall():
#     left_motor.run(200)
#     right_motor.run(200)

def sense_color():
    print(col_sensor.color())
    if col_sensor.color() == Color.GREEN:
        return True
    else:
        return False

def followWall(speed=200):
    """
    The function takes in a speed and distance and makes the robot go straight for that distance at
    that speed

    :param speed: The speed at which the robot will move, defaults to 300 (optional)
    :param distance: The distance you want to travel in meters
    """

    # These are the variables that are used in the PID controller.
    propotional_gain = 2.0
    integral_gain = 0.1
    derevative_gain = 0.01

    # These are the variables that are used in the PID controller.
    distance_integral = 0
    distance_derevative = 0
    last_distance_error = 0
    wait(10)
   # This is the PID controller. It is used to make the robot go straight.
    while r_touch.pressed() is False and l_touch.pressed() is False:
        distance_error = eyes.distance() - 45

        if eyes.distance() > 100:
            # left_motor.run_time(-200, 1000, wait=False)
            # right_motor.run_time(400, 1000)
            break

        # computing the error rate.
        turn_rate = distance_error * propotional_gain
        # correcting the motors speed as needed using PID
        left_motor.run(int(speed - turn_rate))
        right_motor.run(int(speed + turn_rate))
        wait(100)


def wander(theVal):
    # left_motor.run(300 + int(1.8*theVal))
    # right_motor.run(300 - int(1.3*theVal))

    left_motor.run(300)
    right_motor.run(200 + theVal)

    


def foundWall():
    print(eyes.distance())
    if eyes.distance() < 55:
        return True
    else:
        return False


while True:

    foundCol = sense_color()
    if foundCol:
        left_motor.stop()
        right_motor.stop()
        ev3.speaker.say("Fire. Fire. Firee")
        break

    if theTime == 400:
        theTime = 0
        theVal = random.randint(0, 100)
    else:
        theTime += 1

    ff = foundWall()

    if ff:
        followWall()
    else:
        wander(theVal)

    if r_touch.pressed() is True and l_touch.pressed() is True:
        left_motor.run_time(-260, 1000, wait=False)
        right_motor.run_time(-260, 1000)
        if eyes.distance() < 100:
            left_motor.run_angle(200,465, wait=False)
            right_motor.run_angle(200,-465, wait=True)
        else:
            left_motor.run_angle(200,-465, wait=False)
            right_motor.run_angle(200,+465, wait=True)
        

    wait(10)
