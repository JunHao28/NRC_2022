#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# Documentation:
# https://pybricks.com/ev3-micropython/ev3devices.html


# Create your objects here.
ev3 = EV3Brick()
motors = Motors(Motor(Port.a), Motor(Port.b), Motor(Port.c), Motor(Port.d))
sensors = Sensors(GyroSensor(Port.s1), ColorSensor(Port.s2), ColorSensor(Port.s3), ColorSensor(Port.s4),)
Robot(motors, sensors)




# Write your program here.
ev3.speaker.beep()
