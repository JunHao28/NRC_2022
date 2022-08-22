from functions.robot import Robot
from functions.unchanged.StartingPos import StartingPos
import time


def section1(robot):
    # Check Side
    if sum(robot.basic.sense(4)) < 90 and sum(robot.basic.sense(5)) < 90:
        return None
    if sum(robot.basic.sense(4)) > sum(robot.basic.sense(5)):
        robot.startingPos = StartingPos.LEFT
        # -1
    else:
        robot.startingPos = StartingPos.RIGHT
        # 1

    robot.movement.gyrodegree(500, robot.side(250, 100), maximumSpeed=500)
    robot.basic.beep()
    if (robot.startingPos == StartingPos.RIGHT):
        robot.movement.turn(0, -12, oneWheel=2)
    else:
        robot.movement.turn(0, 85, oneWheel=2)
        robot.movement.turn(0, -85, oneWheel=1)
    robot.movement.gyrodegree(400, 700, override=0)
    robot.movement.gyroTillSense(300, lambda: robot.basic.check(1, 250), override=0)
    robot.pause(0.5)
    robot.movement.turn(0, int(robot.startingPos) * 90 - robot.basic.sense(0))
    robot.basic.move(1500, 1500)
    robot.pause(0.8)
    robot.basic.stop()
    return robot
