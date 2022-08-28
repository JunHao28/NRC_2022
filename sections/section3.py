from functions.robot import Robot

def section3(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.neg(90))

    #Detect 4
    condition = lambda: robot.tasks.checkColour(robot.basic.sense(2), robot.basic.sense(4), 2, robot.side(5, 1), special=2)
    robot.movement.gyroTillSense(-300, condition, stopAfter=-100, override=robot.neg(90), stop=False)
    
    #Forward
    robot.movement.gyrodegree(-200, -120, decel=False, stop=False, override=robot.neg(90))
    robot.movement.gyroTillSense(-80, lambda: robot.colour["yellow_floor"].condition(), override=robot.neg(90), stop=False)
    robot.movement.gyrodegree(-200, -130, decel=False, stop=False, override=robot.neg(90))
    
    #Detect 5
    condition = lambda: robot.tasks.checkColour(robot.basic.sense(2), robot.basic.sense(4), 2, 3)
    robot.movement.gyroTillSense(-200, condition, stopAfter=-100, override=robot.neg(90))
    
    robot.pause(0.3)
    robot.motorc.run_angle(300, -195)
    robot.pause(0.3)
    robot.motorb.run_angle(300, -195)
    robot.pause(0.3)
    
    robot.movement.turn(0, 90 - robot.basic.sense(0))
    robot.movement.gyroTillSense(-40, lambda: robot.colour["red_floor"].condition(), override=90, stop=False)
    angleAtDetectRed = robot.motorb.angle()
    robot.movement.gyrodegree(-200, -60, decel=False, stop=False, override=90)

    #Detect 6
    condition = lambda: robot.tasks.checkColour(robot.basic.sense(3), robot.basic.sense(5), 2, 3)
    robot.movement.gyroTillSense(-100, condition, stopAfter=-100, override=robot.neg(90))

    #Align
    robot.movement.gyrodegree(-50, -200 - (robot.motorb.angle() - angleAtDetectRed))
    robot.movement.turn(0, 0 - robot.basic.sense(0), oneWheel=robot.side(2, 0))
    robot.movement.gyrodegree(200, 200)
    robot.moveTillStall(1500)

    return robot