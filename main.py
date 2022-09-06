#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.ev3devices import ColorSensor as Ev3ColorSensor
from pybricks.nxtdevices import ColorSensor as NXTColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import Ev3devSensor
import sys

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
try:
    robot.basic.resetRobot()
    robot.startingPos = StartingPos.RIGHT

    robot.start()
    stopwatch = StopWatch()
    robot.callibrate()
    robot = section1(robot)
    robot.print("time", (stopwatch.time()/1000))
    robot = section2(robot)
    robot.print("time", (stopwatch.time()/1000))
    robot = section3(robot)
    robot.print("time", (stopwatch.time()/1000))
    robot = section4(robot)
    robot.print("time", (stopwatch.time()/1000))
    robot.human = [2, 6]
    robot = section5(robot)
    robot.print("time", (stopwatch.time()/1000))
    if robot != None:
        robot.basic.beep()
        wait(1000)
        robot.motord.run_target(1500, 0)
        robot.print((stopwatch.time()/1000)-1)
except:
    with open('print.txt', 'a') as f:
        f.write("ERROR")
        f.write(str(sys.exc_info()))

# robot.sensor1.reset_angle(0)
# if robot.fire[1] == False or robot.chemical == False:
#     robot.movement.gyroTillSense(150, lambda: robot.colour[robot.side("brown_floor", "blue_floor")].condition(), override=0, stop=False)
#     robot.movement.gyrodegree(1, 50, maximumSpeed=400, minimumSpeed=100, override=0)
#     robot.movement.turn(0, robot.neg(90), oneWheel=robot.side(2, 1))
#     robot.movement.gyrodegree(1, 40, maximumSpeed=400, minimumSpeed=100)
#     if robot.fire[1] == False:
#         robot.basic.beep()
#         robot.tasks.depositWater()
#     elif robot.chemical == False:
#         robot.basic.beep()
#         robot.movement.gyrodegree(1, 320, maximumSpeed=400, minimumSpeed=100)
#         robot.basic.beep()
#         chemical = robot.movement.gyroTillSense(150, lambda: robot.colour["chemical"].condition(robot.basic.sense(2), robot.basic.sense(4)), stopAfter=100)
#         print(chemical)
#         if chemical:
#             robot.movement.gyrodegree(robot.neg(1), robot.neg(220), maximumSpeed=400, minimumSpeed=100)
#             robot.movement.turn(0, 135, oneWheel=1)
#             robot.movement.gyrodegree(-1, -170, maximumSpeed=400, minimumSpeed=20)
#             robot.movement.gyrodegree(1, 130, maximumSpeed=400, minimumSpeed=20)
#             robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
#             robot.movement.gyrodegree(-200, -100, decel=False, stop=False, override=0)
#         # else:
#             # robot.movement.gyrodegree(1, 420, maximumSpeed=600, minimumSpeed=100)
#             # robot.movement.turn(0, 45, oneWheel=1)
#             # robot.movement.gyrodegree(-1, -230, maximumSpeed=400, minimumSpeed=20)
#             # robot.motord.run_target(1500, -200)
#             # robot.movement.gyrodegree(1, 330, maximumSpeed=400, minimumSpeed=20)
#             # robot.movement.turn(0, -robot.basic.sense(0), oneWheel=2)
#             # robot.movement.gyrodegree(-200, -100, decel=False, stop=False, override=0)
#     # robot.movement.gyroTillSense(-160, lambda: not robot.colour["white_floor"].condition(), override=0)
#     # robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=400, pid=robot.movement.track2)
#     # robot.motord.run_target(1500, 0)
#     # robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=250, pid=robot.movement.track2)
# else:
#     robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 200, lambda: False, stopAfter=-150-angleAtDetectBrown, whiteblack=False, pid=robot.movement.track2)
#     robot.movement.turn(0, -40, oneWheel=2)
#     robot.movement.gyrodegree(-1, -300, maximumSpeed=600)
#     robot.motord.run_until_stalled(1500)
#     robot.movement.gyroTillSense(-300, lambda: robot.basic.sense(6) < 10)
#     robot.movement.gyrodegree(1, 70, maximumSpeed=201)
#     robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
#     robot.movement.gyrodegree(1, 200, maximumSpeed=500)
#     robot.movement.moveTillStall(1500)

# robot.tasks.collectChemical(1, 0, special=2)

