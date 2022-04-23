from movements import Robot
from movements import StartingPos
import time

def section1(robot):
    if sum(robot.sensorVal(2)) > 40:
        robot.startingPos = StartingPos.LEFT
    elif sum(robot.sensorVal(3)) > 40:
        robot.startingPos = StartingPos.RIGHT
    else: 
        return None
    robot.pidmovegyrodegree(1000, 500)
    robot.gyroForwardTillSense(500, 1, 250)
    robot.pidturn(200, -50*int(robot.startingPos), oneWheel=(0.5*int(robot.startingPos)+1.5))
    time.sleep(0.1)
    robot.pidturn(200, int(robot.startingPos) * 90 - robot.sensorVal(0))
    robot.move(1500, 1500)
    time.sleep(1.5)
    robot.sensor1.reset_angle(90)
    robot.pidmovegyrodegree(-90, -500)
    robot.gyroForwardTillSense(300, 1, 135)
    robot.pidturn(100, int(robot.startingPos) * -90)
    robot.pidLineTracking(135, 300, 3, 13)
    time.sleep(0.1)
    return robot