#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, GyroSensor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait

from localization import *

# import numpy as np

# from pathFind import *

class TankControls:
    def __init__(self) -> None:
        """
        The function __init__() is a special function in Python classes. It is run as soon as an object
        of a class is instantiated. The self parameter is a reference to the current instance of the
        class, and is used to access variables that belong to the class
        """
       # Initializing the EV3 brick and the motors.
        self.ev3 = EV3Brick()
        self.motor_right = Motor(Port.A)
        self.block_motor = Motor(Port.C)
        self.ultra_motor = Motor(Port.B)
        self.block_motor.reset_angle(0)
        self.motor_left = Motor(Port.D)

        # self.motor_left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        # self.motor_right = Motor(Port.D, Direction.COUNTERCLOCKWISE)

       # Initializing the gyro sensor and resetting the angle to 0.

        self.col_sensor = ColorSensor(Port.S4)
        self.gyro_sensor = GyroSensor(Port.S1)
        self.gyro_sensor.reset_angle(0)
        self.obstacle_sensor = UltrasonicSensor(Port.S3)
        self.ultra_motor.reset_angle(0)

        # self.ev3.speaker.beep()

        self.captured = False

    def repositionUltrasonicSensor(self):
        self.ultra_motor.run_angle(200, 90)
        self.ultra_motor.run_angle(200, 90)
        self.ultra_motor.run_angle(200, -90)
        self.ultra_motor.run_angle(200, -90)
        # self.ultra_motor.run_angle(200, 90)
        # pass

    def captureBlock(self):
        if self.captured:
            pass
        else:
            self.block_motor.run_angle(200, -50)
        self.captured = True

    def releaseBlock(self):
        if self.captured:
            self.block_motor.run_angle(200, 50)
        else:
            pass
        self.captured = False

    def scan_left(self):
        # self.ultra_motor.run_angle(200, 90)
        self.gyro_sensor.reset_angle(0)
        wait(1000)
        d = self.obstacle_sensor.distance()
        # 100 is an approximate distance from sensor to the wall. We can change it later on
        return d

    def scan_forward(self):
        self.ultra_motor.run_angle(400, -90)
        wait(1000)
        d = self.obstacle_sensor.distance()
        return d

    def scan_right(self):
        self.ultra_motor.run_angle(400, -100)
        wait(1000)
        d = self.obstacle_sensor.distance()
        return d

    def position_ultra_left(self):
        self.ultra_motor.run_angle(400, -100)
        wait(1000)

    def position_ultra_right(self):
        self.ultra_motor.run_angle(400, -100)
        wait(1000)

    def returnToPosition(self):
        self.ultra_motor.run_target(180, 0)

    def sense_color(self, colorVal):
        # print(self.col_sensor.color())

        if colorVal.lower() == "blue":
            checkColor = Color.BLUE
        if colorVal.lower() == "green":
            checkColor = Color.GREEN
        if colorVal.lower() == "red":
            checkColor = Color.RED

        return True if self.col_sensor.color() == checkColor else False

    def foundWall(self):
        print(self.obstacle_sensor.distance())
        return True if self.obstacle_sensor.distance() < 70 else False

    def followLeftWall(self, speed=250):
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
            distance_error = self.obstacle_sensor.distance() - 95

            if self.obstacle_sensor.distance() > 100:
                self.go_left()
                self.go_straight()
                self.go_left()
                self.go_straight()

            # computing the error rate
            turn_rate = distance_error * propotional_gain

            # correcting the motors speed as needed using PID
            self.left_motor.run(int(speed - turn_rate))
            self.right_motor.run(int(speed + turn_rate))
            wait(100)
    
    def followRightWall(self, speed=250):
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
            distance_error = self.obstacle_sensor.distance() - 95

            if self.obstacle_sensor.distance() > 100:
                self.go_right()
                self.go_straight()
                self.go_right()
                self.go_straight()

            # computing the error rate
            turn_rate = distance_error * propotional_gain

            # correcting the motors speed as needed using PID
            self.left_motor.run(int(speed - turn_rate))
            self.right_motor.run(int(speed + turn_rate))
            wait(100)

    def go_straight(self, speed=400, distance = 0.305):
        """
        The function takes in a speed and distance and makes the robot go straight for that distance at
        that speed
        :param speed: The speed at which the robot will move, defaults to 300 (optional)
        :param distance: The distance you want to travel in meters
        """
        self.ev3.speaker.beep()

        # These are the variables that are used in the PID controller.
        WHEEL_DIAMETER = 42.2 * 0.1
        # AXLE_TRACK = 200
        PI = 3.141592

        # This is the formula to calculate the number of degrees the robot needs to turn to go a
        # certain distance.
        distance_travelled_by_wheel = WHEEL_DIAMETER * PI
        distance_we_want_to_travel = distance * 100
        total_revolutions_needed = distance_we_want_to_travel / distance_travelled_by_wheel
        total_angle = total_revolutions_needed * 360

        # Resetting the angle of the gyro sensor and the motors to 0.
        self.gyro_sensor.reset_angle(0)
        self.motor_left.reset_angle(0)
        self.motor_right.reset_angle(0)

        # These are the variables that are used in the PID controller.
        propotional_gain = 1.8
        integral_gain = 0.1
        derevative_gain = 0.01

        # These are the variables that are used in the PID controller.
        angle_integral = 0
        angle_derevative = 0
        last_angle_error = 0
        angle_travelled = 0
        wait(10)
       # This is the PID controller. It is used to make the robot go straight.
        while angle_travelled < total_angle:
            if self.tank_controls.sense_color("red") or self.tank_controls.sense_color("blue") or self.tank_controls.sense_color("green") :
                break

            angle_error = self.gyro_sensor.angle() - 0
            angle_integral = angle_integral + angle_error
            angle_derevative = angle_error - last_angle_error

            turn_rate = angle_error * propotional_gain + integral_gain * angle_integral + derevative_gain * angle_derevative
            self.motor_left.run(int(speed - turn_rate))
            self.motor_right.run(int(speed  + turn_rate))

            last_angle_error = angle_error
            angle_travelled  = (self.motor_right.angle() + self.motor_left.angle())/2
            wait(10)
        # Stopping the motors
        self.motor_left.brake()
        self.motor_right.brake()

    def go_left(self, speed=100, rotation=465):
        """
        The robot turns left until the gyro sensor reads -91 degrees
        :param speed: the speed of the motors, defaults to 200 (optional)
        :param rotation: the number of degrees the robot will turn, defaults to 465 (optional)
        """
        self.ev3.speaker.beep()
        # Resetting the angle of the gyro sensor to 0.
        self.gyro_sensor.reset_angle(0)

        # Making the robot turn left.
        self.motor_left.run_angle(speed,-rotation, wait=False)
        self.motor_right.run_angle(speed,rotation, wait=True)

        # This is a while loop that is used to make the robot turn left until the gyro sensor reads
        # -91 degrees.
        angle = self.gyro_sensor.angle()
        while angle != -88:
            if angle < -88:
                self.motor_left.run_angle(100,5, wait=False)
                self.motor_right.run_angle(100,-5, wait=True)
            elif angle > -88:
                self.motor_left.run_angle(100,-5, wait=False)
                self.motor_right.run_angle(100,5, wait=True)
            wait(100)
            angle = self.gyro_sensor.angle()

    def go_right(self, speed=100, rotation=465):
        """
        The robot turns right until the gyro sensor reads 89 degrees
        :param speed: the speed of the motors, defaults to 200 (optional)
        :param rotation: the number of degrees the robot will turn, defaults to 463 (optional)
        """
        self.ev3.speaker.beep()
        # Resetting the angle of the gyro sensor to 0.
        self.gyro_sensor.reset_angle(0)

        # Making the robot turn right.
        self.motor_left.run_angle(speed,rotation, wait=False)
        self.motor_right.run_angle(speed,-rotation, wait=True)

        # This is a while loop that is used to make the robot turn right until the gyro sensor reads
        # 89 degrees.
        angle = self.gyro_sensor.angle()
        while angle != 94:
            if angle < 94:
                self.motor_left.run_angle(100,5, wait=False)
                self.motor_right.run_angle(100,-5, wait=True)
            elif angle > 94:
                self.motor_left.run_angle(100,-5, wait=False)
                self.motor_right.run_angle(100,5, wait=True)
            wait(100)
            angle = self.gyro_sensor.angle()

    def go_backwards(self, speed=400, rotation=463):
        self.ev3.speaker.beep()
        self.motor_left.run_angle(speed,-rotation, wait=False)
        self.motor_right.run_angle(speed,-rotation, wait=True)

    def execute_commands(self, command_string):
        """
        The function takes in a string of commands and executes them one by one
        :param command_string: This is the string of commands that you want to execute
        """
        index_command_string = 0
        while index_command_string < len(command_string):
            if command_string[index_command_string] == 'F':
                count_forward_commands = 1
                count_half_forward_commands = 0
                index_command_string = index_command_string + 1
                while index_command_string < len(command_string) and (command_string[index_command_string] == 'F' or command_string[index_command_string] == 'f'):
                    if command_string[index_command_string] == 'F':
                        count_forward_commands = count_forward_commands + 1
                    elif command_string[index_command_string] == 'f':
                        count_half_forward_commands =  count_half_forward_commands + 1
                    index_command_string = index_command_string + 1
                index_command_string = index_command_string - 1
                self.go_straight(distance = ((0.305*count_forward_commands) + ((0.305/2) * count_half_forward_commands)))


            if command_string[index_command_string] == 'f':
                count_forward_commands = 0
                count_half_forward_commands = 1
                index_command_string = index_command_string + 1
                while index_command_string < len(command_string) and (command_string[index_command_string] == 'F' or command_string[index_command_string] == 'f'):
                    if command_string[index_command_string] == 'F':
                        count_forward_commands = count_forward_commands + 1
                    elif command_string[index_command_string] == 'f':
                        count_half_forward_commands =  count_half_forward_commands + 1
                    index_command_string = index_command_string + 1
                index_command_string = index_command_string - 1
                self.go_straight(speed=250, distance = ((0.305*count_forward_commands) + ((0.305/2) * count_half_forward_commands)))

            if command_string[index_command_string] == 'L':
                self.go_left()
            if command_string[index_command_string] == 'R':
                self.go_right()

            index_command_string = index_command_string + 1

if __name__ == "__main__":
    # init = TankControls()
#     init = Localization((0,0), 'S')
#     init.explore("F F F F")
    # make_a_map = True
    # cntTiles = 1

    # myMap = np.zeros((7,7))
    # print(myMap)
    # world = Workspace()
    # x, y = 0, 0
    # while True:
        # init.repositionUltrasonicSensor()
        # if make_a_map == True:
            # if cntTiles < 43:
    # for i in range(5):
        # leftVal = init.scan_left()
        # frontVal = init.scan_forward()
        # rightVal = init.scan_right()
        # print("tilesOnTheLeft: ", int(leftVal/300))
        # print("tilesInFront: ", int(frontVal/300))
        # print("tilesOnTheRight: ", int(rightVal/300))
        # init.returnToPosition()
                # if init.sense_color("red") or init.sense_color("blue") or init.sense_color("green"):
                    # init.go_backwards()
    init.releaseBlock()
    wait(2000)
    init.captureBlock()
    # init.go_straight()
