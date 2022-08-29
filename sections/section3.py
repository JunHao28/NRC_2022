from functions.robot import Robot

def section3(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.neg(90))

    #Detect 4
    condition = lambda: robot.tasks.checkColour(2, robot.side(5, 1), special=2)
    robot.movement.gyroTillSense(-300, condition, stopAfter=-100, override=robot.neg(90), stop=False)
    robot.tasks.lastSense = [0, 0, 0, 0]
    
    #Forward
    robot.movement.gyrodegree(-200, -120, startingSpeed=350, accelDist=10, deccelDist=80, maximumSpeed=500, minimumSpeed=220, stop=False, override=robot.neg(90))
    robot.movement.gyroTillSense(-160, lambda: robot.colour["yellow_floor"].condition(), override=robot.neg(90), stop=False)
    robot.movement.gyrodegree(-200, -250, startingSpeed=200, accelDist=20, deccelDist=80, maximumSpeed=500, minimumSpeed=240, stop=False, override=robot.neg(90))
    
    #Detect 5
    condition = lambda: robot.tasks.checkColour(2, 3)
    robot.movement.gyroTillSense(-200, condition, stopAfter=-80, override=robot.neg(90))
    robot.tasks.lastSense = [0, 0, 0, 0]
    
    robot.pause(0.1)
    robot.motorc.run_angle(300, -190)
    robot.pause(0.1)
    robot.motorb.run_angle(300, -190)
    robot.pause(0.1)
    
    robot.movement.turn(0, 90 - robot.basic.sense(0))
    robot.movement.gyroTillSense(-100, lambda: robot.colour["red_floor"].condition(), override=90, stop=False)
    angleAtDetectRed = robot.motorb.angle()
    robot.movement.gyrodegree(-200, -60, startingSpeed=150, accelDist=10, deccelDist=40, maximumSpeed=400, minimumSpeed=300, stop=False, override=robot.neg(90))

    #Detect 6
    condition = lambda: robot.tasks.checkColour(3, 3)
    robot.movement.gyroTillSense(-300, condition, stopAfter=-100, override=robot.neg(90))
    robot.tasks.lastSense = [0, 0, 0, 0]

    #Align
    robot.movement.gyrodegree(-160, -210 - (robot.motorb.angle() - angleAtDetectRed), startingSpeed=350, accelDist=10, maximumSpeed=300, times=False, override=robot.neg(90))
    robot.movement.turn(0, 0 - robot.basic.sense(0), oneWheel=robot.side(2, 0))
    robot.movement.gyrodegree(200, 200)
    robot.movement.moveTillStall(1500)

    return robot