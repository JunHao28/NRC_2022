from functions.robot import Robot
from functions.unchanged.StartingPos import StartingPos
from pybricks.parameters import Stop
import time


def section1(robot):

    for i in range(15):
        if robot.basic.sense(0) != 0:
            robot.sensor1.reset_angle(0)

    robot.sensor1.reset_angle(0)
    robot.movement.gyrodegree(1, robot.side(240, 100), maximumSpeed=800, override=0)
    if (robot.startingPos == StartingPos.RIGHT):
        robot.motorb.run_angle(400, 78, then=Stop.BRAKE)
    else:
        robot.movement.turn(0, 85, oneWheel=2)
        robot.movement.turn(0, -85, oneWheel=1)
    robot.movement.decelerate(900)
    robot.movement.turn(0, -robot.basic.sense(0))
    robot.movement.gyroTillSense(300, lambda: robot.basic.check(1, 250))
    robot.movement.gyrodegree(1, 50)
    robot.pause(0.5)
    robot.movement.turn(0, int(robot.startingPos) * 90 - robot.basic.sense(0))
    robot.movement.moveTillStall(1000)
    return robot
