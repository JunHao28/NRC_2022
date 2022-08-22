from movement import Robot
import time

def section3(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.neg(90))

    #Detect 4
    robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(robot.basic.sense(2), 2, robot.side(5, 1), special=2), stopAfter=-80, override=robot.neg(90), stop=False)
    
    #Forward
    robot.movement.gyrodegree(-300, -120, decel=False, stop=False)
    robot.movement.gyroTillSense(-80, lambda: robot.colour["yellow_floor"].condition(), override=robot.neg(90), stop=False)
    robot.movement.gyrodegree(-300, -170, decel=False, stop=False)
    
    #Detect 5
    robot.movement.gyroTillSense(-200, lambda: robot.tasks.checkColour(robot.basic.sense(2), 2, 3), stopAfter=-80, override=robot.neg(90))
    
    robot.motorc.run_angle(300, -180)
    robot.motorb.run_angle(300, -180)
    
    robot.movement.gyrodegree(-300, -50, decel=False, stop=False)

    #Detect 6
    robot.movement.gyroTillSense(-200, lambda: robot.tasks.checkColour(robot.basic.sense(2), 2, 3), stopAfter=-80, override=robot.neg(90))

    #Align
    robot.movement.gyrodegree(-300, -60)
    robot.movement.turn(0, robot.side(-90, 0), oneWheel=robot.side(2, 0))
    robot.basic.move(1000, 1000)
    robot.pause(1)
    robot.basic.stop()