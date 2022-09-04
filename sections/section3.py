from functions.robot import Robot

def section3(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.side(90, 180))
    
    #Detect 4
    condition = lambda: robot.side((robot.tasks.checkColour(3, 1, special=2) or robot.tasks.checkColour(2, 1, special=2)), robot.tasks.checkColour(2, 5, special=2))
    robot.movement.gyroTillSense(-300, condition, stopAfter=-robot.side(100, 80), override=robot.side(90, 0), stop=robot.side(False, True))
    robot.tasks.reset()
    
    #Forward
    if robot.side(True, False):
        robot.movement.gyrodegree(-1, -100, startingSpeed=350, maximumSpeed=600, minimumSpeed=180, stop=False, override=robot.neg(90))
        robot.movement.gyroTillSense(-160, lambda: robot.colour["yellow_floor"].condition(), override=robot.neg(90), stop=False)
        robot.movement.gyrodegree(-1, -170, startingSpeed=160, maximumSpeed=600, minimumSpeed=300, stop=False, override=robot.neg(90))
    else:
        #Move forward
        robot.movement.turn(0, 90-robot.basic.sense(0), oneWheel=2)
        #Move forward
    
    #Detect 5
    condition = lambda: robot.tasks.checkColour(2, 3)
    robot.movement.gyroTillSense(-300, condition, stopAfter=-100, override=robot.neg(90))
    robot.tasks.reset()
    
    robot.pause(0.1)
    robot.motorc.run_angle(300, -195)
    robot.pause(0.1)
    robot.motorb.run_angle(300, -195)
    robot.pause(0.1)
    
    robot.movement.turn(0, 90 - robot.basic.sense(0))
    robot.movement.gyroTillSense(-160, lambda: robot.colour[robot.side("red_floor", "green_floor")].condition(), override=90, stop=False)
    angleAtDetectRedGreen = robot.motorb.angle()
    robot.movement.gyrodegree(-200, -60, startingSpeed=150, accelDist=10, maximumSpeed=400, minimumSpeed=300, stop=False, override=robot.neg(90))

    #Detect 6 
    condition = lambda: robot.tasks.checkColour(3, 3)
    robot.movement.gyroTillSense(-200, condition, stopAfter=-100, override=robot.neg(90))
    robot.tasks.reset()

    #Align
    robot.movement.gyrodegree(-160, -205 - (robot.motorb.angle() - angleAtDetectRedGreen), startingSpeed=350, accelDist=1, maximumSpeed=300, times=False, override=robot.neg(90))
    robot.movement.turn(0, 0 - robot.basic.sense(0), oneWheel=robot.side(2, 0))
    robot.movement.gyrodegree(200, 200, override=0)
    robot.movement.moveTillStall(1500)

    return robot