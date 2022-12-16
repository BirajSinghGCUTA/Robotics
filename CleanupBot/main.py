#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, GyroSensor, ColorSensor, UltrasonicSensor)
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait

from localization import *

class TankControls:
    def __init__(self) -> None:
        """
        The function __init__() is a special function in Python classes. It is run as soon as an object
        of a class is instantiated. The self parameter is a reference to the current instance of the
        class, and is used to access variables that belong to the class
        """
       # Initializing the EV3 brick and the motors.
        self.ev3 = EV3Brick()
        self.right_motor = Motor(Port.A)
        self.block_motor = Motor(Port.C)
        self.ultra_motor = Motor(Port.B)
        self.block_motor.reset_angle(0)
        self.left_motor = Motor(Port.D)

        # self.left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        # self.right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)

       # Initializing the gyro sensor and resetting the angle to 0.

        self.col_sensor = ColorSensor(Port.S4)
        self.gyro_sensor = GyroSensor(Port.S1)
        self.col2_sensor = ColorSensor(Port.S2)
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
        print("following left wall")
        detectedColor = False
        while True:
            self.ev3.screen.clear()
            self.ev3.screen.draw_text(40, 50, "Following left wall")
            bot_left = self.scan_left()
            bot_forward = self.scan_forward()
            bot_right = self.scan_right()
            self.returnToPosition()
            print("front:", bot_forward)
            print("left:", bot_left)
            colorIsBlue = self.sense_color(colorVal="blue")
            if bot_forward > 55:
                if colorIsBlue:
                    detectedColor = True
                else:
                    if bot_left > 150:
                        self.go_left()
                        self.go_straight()
                        self.go_left()
                        self.go_straight()

                    self.go_straight()
                    
                if detectedColor:
                    self.go_straight()
                    # self.go_backwards()
                    self.go_left()
                    self.go_left()
                    self.ev3.screen.clear()
                    self.ev3.screen.draw_text(40, 50, "Found Blue location")
                    return "blue"
                    # break
                wait(100)
            else:
                self.go_right()
                wait(100)
    
    def followRightWall(self, speed=250):
        detectedColor = False
        while True:
            self.ev3.screen.clear()
            self.ev3.screen.draw_text(40, 50, "Following right wall")
            # print("following right wall")
            bot_left = self.scan_left()
            bot_forward = self.scan_forward()
            bot_right = self.scan_right()
            self.returnToPosition()
            print("front:", bot_forward)
            print("right:", bot_right)
            colorIsRed= self.sense_color(colorVal="red")
            if bot_forward > 55 or (bot_forward < 55 and bot_right > 150):
                if colorIsRed:
                    detectedColor = True
                else:
                    if bot_right > 150:
                        self.go_right()
                        self.go_straight()
                        self.go_right()
                        self.go_straight()

                    print("going straight")
                    self.go_straight()

                if detectedColor:
                    self.go_straight()
                    self.go_backwards()
                    self.go_left()
                    self.go_left()
                    self.ev3.screen.clear()
                    self.ev3.screen.draw_text(40, 50, "Found Red location")
                    return "red"
                    # break
                wait(100)
            else:
                self.go_left()
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
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)

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
            if self.sense_color("red") or self.sense_color("blue") or self.sense_color("green") :
                break

            angle_error = self.gyro_sensor.angle() - 0
            angle_integral = angle_integral + angle_error
            angle_derevative = angle_error - last_angle_error

            turn_rate = angle_error * propotional_gain + integral_gain * angle_integral + derevative_gain * angle_derevative
            self.left_motor.run(int(speed - turn_rate))
            self.right_motor.run(int(speed  + turn_rate))

            last_angle_error = angle_error
            angle_travelled  = (self.right_motor.angle() + self.left_motor.angle())/2
            wait(10)
        # Stopping the motors
        self.left_motor.brake()
        self.right_motor.brake()
    
    def count_tiles(self, distance):
        if(distance >= 2550 or distance <= 250):
            return 0
        elif (distance > 250 and distance < 305):
            return 1
        else:
            return int(distance / 305)

    # def getHemisphere(self):
        bot_left = self.scan_left()
        bot_forward = self.scan_forward()
        bot_right = self.scan_right()
        self.returnToPosition()

        left_tile_count = self.count_tiles(bot_left)
        right_tile_count = self.count_tiles(bot_right)
        forward_tile_count = self.count_tiles(bot_forward)

        hemisphere = ''
        hDist = left_tile_count + right_tile_count + 1
        if hDist > 4:
            hemisphere = 'b'
        elif hDist == 4:
            if forward_tile_count == 0:
                hemisphere = 't'
            else:
                self.go_straight()
                bot_left = self.scan_left()
                bot_forward = self.scan_forward()
                bot_right = self.scan_right()
                self.returnToPosition()
                left_tile_count = self.count_tiles(bot_left)
                right_tile_count = self.count_tiles(bot_right)
                hDist = left_tile_count + right_tile_count + 1
                hemisphere = 't' if hDist < 4 else 'b'
        else:
            hemisphere = 't'

        return hemisphere

    # def approach_wall(self, alreadyLocalized = False):
        bot_left = self.scan_left()
        bot_forward = self.scan_forward()
        bot_right = self.scan_right()
        self.returnToPosition()
        forward_tile_count = self.count_tiles(bot_forward)

        if alreadyLocalized:
            hemi = self.getHemisphere()
            bot_left = self.scan_left()
            bot_forward = self.scan_forward()
            bot_right = self.scan_right()
            self.returnToPosition()

            if hemi == 't':
                for n in range(forward_tile_count):
                    self.go_straight()
                self.go_right()
                color = self.followLeftWall()
                
            if hemi == 'b':
                self.go_left()
                self.go_left()
                bot_left = self.scan_left()
                bot_forward = self.scan_forward()
                bot_right = self.scan_right()
                self.returnToPosition()
                forward_tile_count = self.count_tiles(bot_forward)

                for n in range(forward_tile_count):
                    self.go_straight()
                self.go_left()
                color = self.followRightWall()
        else:
            for n in range(forward_tile_count):
                self.go_straight()
            self.go_right()
            color = self.followLeftWall()

        return color

    def approach_wall(self):
        # bot_left = self.scan_left()
        # bot_forward = self.scan_forward()
        # bot_right = self.scan_right()
        # self.returnToPosition()
        # forward_tile_count = self.count_tiles(bot_forward)
        
        # if alreadyLocalized:
        #     print("Localized")
        #     if current_coordinate == (0,0) and current_heading=='E':
        #         return "Explore"
        #     else:
        #         for n in range(forward_tile_count):
        #             self.go_straight()
        #         self.go_left()
        #         color = self.followRightWall()
        # else:
        print("Not localized yet")
        while True:
            bot_left = self.scan_left()
            bot_forward = self.scan_forward()
            bot_right = self.scan_right()
            self.returnToPosition()
            if bot_left < 150 and bot_right < 150:
                self.go_left()
                self.go_left()
            elif bot_left < 150 and bot_forward > 60:
                color = self.followLeftWall()
                break
            elif bot_right < 150 and bot_forward > 60:
                color = self.followRightWall()
                break
            elif bot_forward > 55:
                print(bot_forward, ">55")
                if bot_left < bot_forward and bot_left < bot_right:
                    self.go_left()
                if bot_right < bot_forward and bot_right < bot_left:
                    self.go_right()

                if bot_forward < bot_left and bot_forward < bot_right:
                    self.go_straight()
            else:
                print(bot_forward, bot_left, bot_right)
                
        return color



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
        self.left_motor.run_angle(speed,-rotation, wait=False)
        self.right_motor.run_angle(speed,rotation, wait=True)

        # This is a while loop that is used to make the robot turn left until the gyro sensor reads
        # -91 degrees.
        angle = self.gyro_sensor.angle()
        while angle != -88:
            if angle < -88:
                self.left_motor.run_angle(100,5, wait=False)
                self.right_motor.run_angle(100,-5, wait=True)
            elif angle > -89:
                self.left_motor.run_angle(100,-5, wait=False)
                self.right_motor.run_angle(100,5, wait=True)
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
        self.left_motor.run_angle(speed,rotation, wait=False)
        self.right_motor.run_angle(speed,-rotation, wait=True)

        # This is a while loop that is used to make the robot turn right until the gyro sensor reads
        # 89 degrees.
        angle = self.gyro_sensor.angle()
        while angle != 93:
            if angle < 93:
                self.left_motor.run_angle(100,5, wait=False)
                self.right_motor.run_angle(100,-5, wait=True)
            elif angle > 93:
                self.left_motor.run_angle(100,-5, wait=False)
                self.right_motor.run_angle(100,5, wait=True)
            wait(100)
            angle = self.gyro_sensor.angle()

    def go_backwards(self, speed=400, rotation=463):
        self.ev3.speaker.beep()
        self.left_motor.run_angle(speed,-rotation, wait=False)
        self.right_motor.run_angle(speed,-rotation, wait=True)

    def execute_commands(self, command_string):
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
    my_tank = TankControls()
    detected_color = my_tank.approach_wall()

    if detected_color == "red":
        init = Localization((0,0), 'E')
        init.explore()
    else:
        init = Localization((6,0), 'W')
        init.explore()
