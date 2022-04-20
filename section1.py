from movements import Robot
from movements import StartingPos

def section1(robot):
    print("true")
    if sum(robot.sensorVal(2)) > 40:
        robot.startingPos = StartingPos.LEFT
    elif sum(robot.sensorVal(3)) > 40:
        robot.startingPos = StartingPos.RIGHT
    else: 
        return None
    robot.pidmovegyrodegree(1000, 500)
    robot.gyroForwardTillSense(500, 0, 135)
    robot.pidturn(500, 90)
    robot.move(500, 500)
    return robot