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
    robot.beep()
    robot.gyroForwardTillSense(500, 0, 250)
    robot.pidturn(200, -40, oneWheel=(0.5*int(robot.startingPos)+1.5))
    time.sleep(0.3)
    robot.pidturn(200, int(robot.startingPos) * 90 - robot.sensorVal(0))
    robot.move(1000, 1000)
    time.sleep(1)
    robot.sensor1.reset_angle(90)
    robot.pidmovegyrodegree(-100, -500)
    robot.gyroForwardTillSense(500, 0, 135)
    robot.pidturn(100, int(robot.startingPos) * -90)
    time.sleep(0.1)
    return robot