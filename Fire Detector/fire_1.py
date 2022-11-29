#!/usr/bin/env pybricks-micropython
import random

from pybricks.ev3devices import (ColorSensor, Motor, TouchSensor,
                                 UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.tools import wait


class Firefighter:
    def __init__(self) -> None:
        self.ev3 = EV3Brick()

        # Initialize Sensors & Motors
        self.col_sensor = ColorSensor(Port.S1)
        self.l_touch = TouchSensor(Port.S2)
        self.r_touch = TouchSensor(Port.S3)
        self.eyes = UltrasonicSensor(Port.S4)

        self.left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)


        self.randomValue = 0
        self.myTempTime = 0
        self.previousRandomValue = 0

        self.ev3.speaker.say("Here we go again")

    def sense_color(self):
        print(self.col_sensor.color())
        return True if self.col_sensor.color() == Color.GREEN else False

    def foundWall(self):
        print(self.eyes.distance())
        return True if self.eyes.distance() < 70 else False

    def followWall(self, speed=250):
        """
        The function takes in a speed and distance and makes the robot go straight for that distance at
        that speed

        :param speed: The speed at which the robot will move, defaults to 300 (optional)
        :param distance: The distance you want to travel in meters
        """

        # These are the variables that are used in the PID controller.
        propotional_gain = 0.8
        integral_gain = 0.1
        derevative_gain = 0.01

        # These are the variables that are used in the PID controller.
        distance_integral = 0
        distance_derevative = 0
        last_distance_error = 0
        wait(10)

        # This is the PID controller. It is used to make the robot go straight.
        while self.r_touch.pressed() is False and self.l_touch.pressed() is False:
            distance_error = self.eyes.distance() - 45

            if self.eyes.distance() > 100:
                # left_motor.run_time(-200, 1000, wait=False)
                # right_motor.run_time(400, 1000)
                break

            # computing the error rate.
            turn_rate = distance_error * propotional_gain

            # correcting the motors speed as needed using PID
            self.left_motor.run(int(speed - turn_rate))
            self.right_motor.run(int(speed + turn_rate))
            wait(100)

    def wander(self, randomValue):
        self.left_motor.run(400+int(1.5*randomValue))
        self.right_motor.run(400-int(randomValue))

    def bumperPressed(self):
        return True if (self.r_touch.pressed() is True) and (self.l_touch.pressed() is True) else False

if __name__ == "__main__":
    myrobot = Firefighter()
    while True:
        foundCol = myrobot.sense_color()
        if foundCol:
            myrobot.left_motor.stop()
            myrobot.right_motor.stop()
            myrobot.ev3.speaker.say("Fire Fire Fire.")
            break

        if myrobot.myTempTime == 350:
            myrobot.randomValue = -1*random.randint(50, 150) if myrobot.previousRandomValue >= 0 else random.randint(50, 150)
            myrobot.previousRandomValue = myrobot.randomValue
            myrobot.myTempTime = 0
        else:
            myrobot.myTempTime += 1

        itFoundAWall = myrobot.foundWall()

        if itFoundAWall:
            myrobot.followWall()
            wait(100)
            check = myrobot.bumperPressed()
            if check:
                myrobot.left_motor.run_time(-260, 1000, wait=False)
                myrobot.right_motor.run_time(-260, 1000)
                if myrobot.eyes.distance() < 100:
                    myrobot.left_motor.run_angle(200, 465, wait=False)
                    myrobot.right_motor.run_angle(200, -465, wait=True)
                else:
                    myrobot.left_motor.run_angle(200, -465, wait=False)
                    myrobot.right_motor.run_angle(200, 465, wait=True)
        else:
            myrobot.wander(myrobot.randomValue)

            check = myrobot.bumperPressed()

            if check:
                myrobot.left_motor.run_time(-260, 1000, wait=False)
                myrobot.right_motor.run_time(-260, 1000)
                
                if random.randint(0,1) == 0:
                    myrobot.left_motor.run_angle(200, 465, wait=False)
                    myrobot.right_motor.run_angle(200, -465, wait=True)
                else:
                    myrobot.left_motor.run_angle(200,-465, wait=False)
                    myrobot.right_motor.run_angle(200, 465, wait=True)

        

        wait(10)
