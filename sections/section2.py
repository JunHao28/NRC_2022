from functions.robot import Robot
import time

def section2(robot):
    if robot == None:
        return robot
    
    #Reset Angle
    robot.sensor1.reset_angle(robot.side(90, 270))

    robot.movement.gyrodegree(-1, robot.side(-175, -160), maximumSpeed=400, override=robot.side(90, 270))
    robot.pause(0.1)
    robot.movement.turn(0, (180)-robot.basic.sense(0), oneWheel=robot.side(2, 1))
    
    #Line tracking
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 300, lambda: robot.colour[robot.side("blue_floor", "brown_floor")].condition(), pid=robot.movement.track2)

    #Face 180°
    robot.movement.turn(0, (180) - robot.basic.sense(0))

    #Detect 1
    robot.print("1:")
    condition = lambda: robot.tasks.checkColour(2, robot.side(6, 2))
    returnVal = robot.movement.gyroTillSense(-250, condition, stopAfter=-250, override=180, stop=False)
    robot.tasks.reset()

    #Move forward
    robot.movement.gyrodegree(-1, -180, stop=False, override=180, maximumSpeed=600, minimumSpeed=200, startingSpeed=(0 if returnVal else 250))
    robot.movement.gyroTillSense(-200, lambda: robot.colour[robot.side("green_floor", "red_floor")].condition(), override=180, stop=False)
    angleAtDetectGreen = robot.motorb.angle()
    returnVal=False

    #Detect 2
    robot.print("2:")
    condition = lambda: robot.tasks.checkColour(2, robot.side(6, 2), special=1)
    returnVal = robot.movement.gyroTillSense(-250, condition, stopAfter=-140, override=180, stop=False)
    robot.tasks.reset()

    #Move Forward
    robot.movement.gyrodegree(-1, -30, stop=False, startingSpeed=(250 if not returnVal else 0), override=180, accelDist=1, maximumSpeed=201)

    #Detect 3
    robot.print("3:")
    if int(robot.startingPos) == 1:
        robot.movement.gyroTillSense(-200, lambda: robot.tasks.checkColour(2, 5, special=1), stopAfter=-100, override=180, stop=True)
        robot.tasks.reset()
    robot.basic.stop()
    robot.pause(1)
    robot.movement.gyrodegree(-1, -robot.side(265, 200) - (robot.motorb.angle() - angleAtDetectGreen), startingSpeed=0, maximumSpeed=150, minimumSpeed=100, override=180)
    robot.movement.turn(0, robot.side(90, 270)-robot.basic.sense(0), oneWheel=robot.side(2, 1))
    if robot.startingPos == -1:
        robot.movement.gyrodegree(-100, 5, decel=False, override=270)
        robot.movement.turn(0, 360-robot.basic.sense(0), oneWheel=2)
    robot.movement.moveTillStall(400)
    robot.pause(0.7)    
    return robot