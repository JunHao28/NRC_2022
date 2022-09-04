from functions.robot import Robot
import time

def section2(robot):
    if robot == None:
        return robot
    
    #Reset Angle
    robot.sensor1.reset_angle(robot.neg(90))

    robot.movement.gyrodegree(-1, robot.side(-175, -160), maximumSpeed=300, override=robot.neg(90))
    robot.pause(0.1)
    robot.movement.turn(0, 180-robot.basic.sense(0), oneWheel=robot.side(2, 1))
    
    #Line tracking
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 300, lambda: robot.colour[robot.side("blue_floor", "brown_floor")].condition())

    #Face 180°
    robot.movement.turn(0, robot.neg(180) - robot.basic.sense(0))

    #Detect 1
    print("1:")
    condition = lambda: robot.tasks.checkColour(2, robot.side(6, 2))
    returnVal = robot.movement.gyroTillSense(-300, condition, stopAfter=-250, override=180, stop=False)
    robot.tasks.reset()

    #Move forward
    robot.movement.gyrodegree(-1, -180, stop=False, override=180, maximumSpeed=600, minimumSpeed=160, startingSpeed=(0 if returnVal else 350))
    robot.movement.gyroTillSense(-160, lambda: robot.colour[robot.side("green_floor", "red_floor")].condition(), override=180, stop=False)
    angleAtDetectGreen = robot.motorb.angle()

    #Detect 2
    print("2:")
    condition = lambda: robot.tasks.checkColour(2, robot.side(6, 2), special=1)
    robot.movement.gyroTillSense(-300, condition, stopAfter=-140, override=180, stop=False)
    robot.tasks.reset()

    #Move Forward
    robot.movement.gyrodegree(-1, -30, stop=False, override=180, accelDist=1, maximumSpeed=201)

    #Detect 3
    print("3:")
    if int(robot.startingPos) == 1:
        returnVal = robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(2, 5, special=1), stopAfter=-100, override=robot.neg(180), stop=False)
        robot.movement.gyrodegree(-1, -250 - (robot.motorb.angle() - angleAtDetectGreen), startingSpeed=0 if returnVal else 250, maximumSpeed=250, minimumSpeed=160, times=False)
        robot.tasks.reset()
    robot.movement.turn(0, robot.side(robot.basic.sense(0) - 270, -robot.basic.sense(0)), oneWheel=robot.side(2, 0))
    robot.movement.moveTillStall(1500)
    
    return robot