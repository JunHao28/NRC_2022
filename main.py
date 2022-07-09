#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.ev3devices import ColorSensor as Ev3ColorSensor                                 
from pybricks.nxtdevices import ColorSensor as NxtColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
# import sys

# sys.path.append('../')

from functions.robot import Robot


#Program Files
from sections.section1 import section1
from sections.section2 import section2
from functions.unchanged.StartingPos import StartingPos

# Documentation:
# https://pybricks.com/ev3-micropython/ev3devices.html


# Create your objects here.
ev3 = EV3Brick()
# robot = Robot(ev3, [Motor(Port.B), Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE), Motor(Port.D)], [GyroSensor(Port.S1), Ev3ColorSensor(Port.S2), NxtColorSensor(Port.S3), NxtColorSensor(Port.S4)])
robot = Robot(ev3, [0, 0, 0], [0, 0, 0, 0])
# robot = Robot(ev3, [Motor(Port.B), Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE), Motor(Port.D)], [GyroSensor(Port.S1), Ev3ColorSensor(Port.S2), NXTColorSensor(Port.S3), NXTColorSensor(Port.S4)])
robot.movement.sound()


#NOTE: reset arm position
# robot.resetRobot()
ev3.speaker.beep()
robot.startingPos = StartingPos.RIGHT
# robot = section1(robot)
# robot = section2(robot)
# def checkCondition():
#     return False
# condition = checkCondition
# robot.turn(0, 90, oneWheel=2)
# robot.pidmovegyrodegree(160, -700)

time.sleep(1)
# robot.pidmovegyrodegree(-1500, -200)
# robot.turn(0, 90, oneWheel=0)
# robot.stop()
# robot.beep()
# time.sleep(1)
# print(robot.sensorVal(2))

#(25, 18, 7)

# robot.turn(0, 90, oneWheel=1)
# print(robot.sensor2.rgb())
# robot.pidLineTracking(25, 300)

# robot.collectChemical(2)
# print(robot.sensorVal(3))
# print(robot.sensor2.reflection())
# robot.checkColour(robot.sensorVal(3), 2, 1)



# Write your program here.
# Motor(Port.D).run(10000)
# time.sleep(1.2)
# Motor(Port.D).run(-10000)
# time.sleep(0.7)
# Motor(Port.D).run(10000)
# time.sleep(1.2)
# Motor(Port.D).run(-10000)
# time.sleep(0.7)
# Motor(Port.D).brake()

# color = robot.gyroForwardTillSense(300, 0, 5, stopAfter=200)
# if color[0] >= 10 and color[1] <= 10 and color[2] <= 10:
#     robot.depositWater()
# else: 
#     print(color)
#     print()
# robot.stop()
# robot.pidmovegyrodegree(200, 700)
# robot.depositWater()
# robot.stop()
# robot.beep()
