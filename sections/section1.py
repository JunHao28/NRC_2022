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

    robot.movement.gyrodegree(1, robot.side(210, 100), maximumSpeed=800, override=0)
    if (robot.startingPos == StartingPos.RIGHT):
        robot.motorb.run_angle(400, 70)
    else:
        robot.movement.turn(0, 85, oneWheel=2)
        robot.movement.turn(0, -85, oneWheel=1)
    # robot.movement.gyrodegree(1000, 700, override=0, maximumSpeed=1500)
    robot.movement.decelerate(900)
    robot.movement.gyroTillSense(300, lambda: robot.basic.check(1, 250))
    robot.movement.gyrodegree(1, 50)
    robot.pause(0.5)
    robot.movement.turn(0, int(robot.startingPos) * 90 - robot.basic.sense(0))
    robot.movement.moveTillStall(1000)
    return robot
