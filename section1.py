from movements import Robot
from movements import StartingPos
import time

def section1(robot):
    if sum(robot.sensorVal(2)) > 50:
        robot.startingPos = StartingPos.LEFT
    elif sum(robot.sensorVal(3)) > 50:
        robot.startingPos = StartingPos.RIGHT
    else: 
        return None
    robot.pidmovegyrodegree(300, 1500)
    robot.pidturn(0, -10*int(robot.startingPos), oneWheel=(0.5*int(robot.startingPos)+1.5))
    robot.pidmovegyrodegree(700, 1000)
    robot.gyroForwardTillSense(1500, 1, 250)
    time.sleep(0.5)
    robot.pidturn(0, int(robot.startingPos) * 90 - robot.sensorVal(0))
    print("Angle Before Alignment:", robot.sensorVal(0))
    robot.move(1500, 1500)
    time.sleep(1.0)
    robot.sensor1.reset_angle(int(robot.startingPos) * 90)
    return robot