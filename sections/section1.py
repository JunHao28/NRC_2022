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

    robot.movement.gyrodegree(400, robot.side(170, 100), maximumSpeed=700, override=0, minimumSpeed=400, deccelDist=130)
    if (robot.startingPos == StartingPos.RIGHT):
        robot.motorb.run_angle(400, 100)
    else:
        robot.movement.turn(0, 85, oneWheel=2)
        robot.movement.turn(0, -85, oneWheel=1)
    robot.movement.gyrodegree(600, 700, override=0)
    robot.movement.gyroTillSense(300, lambda: robot.basic.check(1, 250), override=0)
    robot.movement.gyrodegree(300, 100)
    robot.pause(0.5)
    robot.movement.turn(0, int(robot.startingPos) * 90 - robot.basic.sense(0))
    robot.movement.moveTillStall(1500)
    return robot
