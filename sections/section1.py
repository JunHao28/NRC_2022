from functions.robot import Robot
from functions.unchanged.StartingPos import StartingPos
import time


def section1(robot):

    # Check Side
    if sum(robot.basic.sense(2)) < 70 and sum(robot.basic.sense(3)) < 70:
        return None
    if sum(robot.sense(2)) > sum(robot.sense(3)):
        robot.startingPos = StartingPos.LEFT
        # -1
    else:
        robot.startingPos = StartingPos.RIGHT
        # 1

    robot.movement.gyrodegree(1500, 300 if robot.startingPos == 1 else 100)
    if (robot.startingPos == StartingPos.RIGHT):
        robot.turn(0, -12, oneWheel=2)
    else:
        robot.turn(0, 85, oneWheel=1)
        robot.turn(0, -85, oneWheel=2)
    robot.gyrodegree(1500, 700)
    robot.gyroTillSense(800, lambda: robot.basic.check(1, 250))
    robot.wait(0.5)
    robot.turn(0, int(robot.startingPos) * 90 - robot.sense(0))
    robot.move(1500, 1500)
    robot.wait(0.8)
    robot.stop()
    return robot
