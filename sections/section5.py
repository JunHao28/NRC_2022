from functions.robot import Robot

def section5(robot):
    if robot == None:
        return robot

    robot.sensor1.reset_angle(-90)
    robot.movement.gyrodegree(-200, -200, decel=False, stop=False, override=-90)
    robot.movement.gyroTillSense(-80, lambda: robot.colour["white_floor"].condition(), override=-90, stop=False)
    # angleAtDetectWhite = robot.motorb.angle()
    # robot.movement.gyrodegree(-200, -390 - (robot.motorb.angle() - angleAtDetectWhite), override=-90)
    robot.movement.gyrodegree(-200, -410, override=-90)
    robot.movement.turn(0, -robot.basic.sense(0), oneWheel=robot.side(2, 0))
    robot.pause(0.5)
    robot.movement.gyroTillSense(-100, lambda: robot.tasks.checkColour(2, 2, special=2), stopAfter=-100, override=0, stop=True)
    robot.tasks.lastSense = [0, 0, 0, 0]
    
    robot.movement.turn(0, - robot.basic.sense(0), oneWheel=1)
    robot.movement.gyrodegree(-300, -190, decel=False, stop=False, override=0)
    robot.basic.beep()
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 200, lambda: robot.tasks.checkColour(3, 2), stopAfter=200)
    robot.tasks.lastSense = [0, 0, 0, 0]
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 300, lambda: False, stopAfter=250)
    robot.motord.run_target(1500, 0)
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 400, lambda: False, stopAfter=100)
    robot.movement.gyrodegree(-300, -100, override=0)
    robot.movement.turn(0, -90, oneWheel=1)
    robot.movement.gyrodegree(300, 400)
    robot.movement.moveTillStall(1500)
    robot.sensor1.reset_angle(-90)
    robot.movement.gyrodegree(-200, -10)
    robot.movement.turn(0, -90, oneWheel=2)
    robot.movement.gyrodegree(400, 800)
    
    robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=2)
    robot.movement.moveTillStall(1500)
    return robot