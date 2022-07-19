#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.ev3devices import ColorSensor as Ev3ColorSensor                                 
from pybricks.nxtdevices import ColorSensor as NXTColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch

#Program Files
from functions.robot import Robot
from sections.section1 import section1
from sections.section2 import section2
from functions.unchanged.StartingPos import StartingPos

# Documentation:
# https://pybricks.com/ev3-micropython/ev3devices.html


# Create your objects here.
stopwatch = StopWatch()
ev3 = EV3Brick()
# robot = Robot(ev3, [Motor(Port.B), Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE), Motor(Port.D)], [GyroSensor(Port.S1), Ev3ColorSensor(Port.S2), NxtColorSensor(Port.S3), NxtColorSensor(Port.S4)], lambda: wait())
# robot = Robot(ev3, [0, 0, 0], [0, 0, 0, 0])
robot = Robot(ev3, [Motor(Port.B), Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE), Motor(Port.D)], [GyroSensor(Port.S1), Ev3ColorSensor(Port.S2), NXTColorSensor(Port.S3), NXTColorSensor(Port.S4)], lambda time: wait(time))
# robot.basic.sound()


#NOTE: reset arm position
robot.basic.resetRobot()
# robot.startingPos = StartingPos.RIGHT
# robot.movement.turn(0, 90)
# robot.movement.gyrodegree(1500, 900)
robot = section1(robot)
robot = section2(robot)
wait(1000)
print((stopwatch.time()/1000)-1)


