#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.ev3devices import ColorSensor as Ev3ColorSensor
from pybricks.nxtdevices import ColorSensor as NXTColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import Ev3devSensor

#Program Files
from functions.robot import Robot
from sections.section1 import section1
from sections.section2 import section2
from sections.section3 import section3
from sections.section4 import section4
from sections.section5 import section5
from functions.unchanged.StartingPos import StartingPos

# Documentation:
# https://pybricks.com/ev3-micropython/ev3devices.html


# Create your objects here.
stopwatch = StopWatch()
ev3 = EV3Brick()

motorb = Motor(Port.B)
motorc = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
motord = Motor(Port.D)
gyro = GyroSensor(Port.S1)
sensor1 = Ev3ColorSensor(Port.S2)
sensor2 = Ev3devSensor(Port.S3)
sensor3 = Ev3devSensor(Port.S4)
robot = Robot(ev3, [motorb, motorc, motord], [gyro, sensor1, sensor2, sensor3], lambda time: wait(time))


#NOTE: reset arm position
robot.basic.resetRobot()
# robot.startingPos = StartingPos.RIGHT
# robot.start()
# robot.callibrate()
robot = section1(robot)
print("time", (stopwatch.time()/1000))
robot = section2(robot)
print("time", (stopwatch.time()/1000))
robot = section3(robot)
print("time", (stopwatch.time()/1000))
robot = section4(robot)
print("time", (stopwatch.time()/1000))
robot.human = [1, 6]
robot = section5(robot)
print("time", (stopwatch.time()/1000))
if robot != None:
    wait(1000)
    robot.motord.run_target(1500, 0)
    print((stopwatch.time()/1000)-1)


