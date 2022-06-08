from movements import Robot
from movements import StartingPos
import time

def section1(robot):
    if sum(robot.sensorVal(2)) > 70:
        robot.startingPos = StartingPos.LEFT
        #-1
    elif sum(robot.sensorVal(3)) > 70:
        robot.startingPos = StartingPos.RIGHT
        #1
    else: 
        return None
    robot.pidmovegyrodegree(100*int(robot.startingPos)+200, 1500)
    if (robot.startingPos == StartingPos.RIGHT):
        robot.pidturn(0, -15, oneWheel=2)
    else:
        robot.pidturn(0, 85, oneWheel=1)
        robot.pidturn(0, -85, oneWheel=2)
    robot.pidmovegyrodegree(700, 1000)
    robot.gyroForwardTillSense(700, 1, 250)
    time.sleep(0.5)
    robot.pidturn(0, int(robot.startingPos) * 90 - robot.sensorVal(0))
    robot.move(1500, 1500)
    time.sleep(1)
    robot.stop()
    return robot