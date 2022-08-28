from functions.robot import Robot
import time

def section2(robot):
    if robot == None:
        return robot
    
    #Reset Angle
    robot.sensor1.reset_angle(robot.neg(90))

    robot.movement.gyrodegree(-150, robot.side(-175, -160), maximumSpeed=300, decel=False, override=robot.neg(90))
    robot.pause(0.1)
    robot.movement.turn(0, robot.basic.sense(0), oneWheel=robot.side(2, 1))
    
    #Line tracking
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 300, lambda: robot.colour[robot.side("blue_floor", "brown_floor")].condition())

    #Face 180°
    robot.movement.turn(0, robot.neg(180) - robot.basic.sense(0))

    print(robot.basic.sense(4))

    #Detect 1
    condition = lambda: robot.tasks.checkColour(robot.basic.sense(2), robot.basic.sense(4), 2, robot.side(6, 2))
    print("1")
    returnVal = robot.movement.gyroTillSense(-300, condition, stopAfter=-250, override=180, stop=False)

    print(returnVal)
    #Move forward
    robot.movement.gyrodegree(-100, -180, stop=False, override=180, maximumSpeedAccel=400, minimumSpeed=240, startingSpeed=(350 if returnVal != True else 0), decelDist=110)
    robot.movement.gyroTillSense(-160, lambda: robot.colour[robot.side("green_floor", "red_floor")].condition(), override=180, stop=False)
    angleAtDetectGreen = robot.motorb.angle()

    #Detect 2
    condition = lambda: robot.tasks.checkColour(robot.basic.sense(2), robot.basic.sense(4), 2, robot.side(6, 2), special=1)
    print("2")
    robot.movement.gyroTillSense(-300, condition, stopAfter=-140, override=180, stop=False)

    #Move Forward
    robot.movement.gyrodegree(-200, -30, stop=False, override=180)

    #Detect 3
    if int(robot.startingPos) == 1:
        robot.movement.gyroTillSense(-200, lambda: robot.tasks.checkColour(robot.basic.sense(2),robot.basic.sense(4), 2, 5, special=1), stopAfter=-100, override=robot.neg(180), stop=False)
        robot.movement.gyrodegree(100, -260 - (robot.motorb.angle() - angleAtDetectGreen), startingSpeed=150, maximumSpeedAccel=150, minimumSpeed=80, decelDist=10, times=False)
    robot.movement.turn(0, robot.basic.sense(0) - 270, oneWheel=robot.side(2, 0))
    robot.moveTillStall(1500)
    
    return robot