from functions.robot import Robot


def section4(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.neg(0))

    #Detect 7 + 8
    condition = lambda: robot.tasks.checkColour(3, 1, special=2) or robot.tasks.checkColour(2, 1, special=2)
    robot.movement.gyroTillSense(-300, condition, stopAfter=-80, override=0)
    robot.tasks.reset()
    

    robot.movement.gyrodegree(-1, -220, maximumSpeed=400, minimumSpeed=150, stop=False, override=0)
    robot.movement.gyroTillSense(-150, lambda: robot.colour["brown_floor"].condition(), override=0, stop=False)
    robot.movement.gyrodegree(-1, -185, startingSpeed=150, maximumSpeed=400, minimumSpeed=250, stop=False, override=0)

    robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(3, 2, special=2), stopAfter=-80, override=0, stop=False)
    robot.tasks.reset()
    robot.movement.gyrodegree(-200, -230, maximumSpeed=500, minimumSpeed=80, stop=False, override=0)
    robot.motorb.run_angle(1500, -100, )
    robot.motorc.run_angle(1500, -100, )
    robot.movement.gyroTillSense(-80, lambda: (not robot.colour["brown_floor"].condition()), override=0, stop=False)
    angleAtDetectBrown = robot.motorb.angle()
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 200, lambda: robot.tasks.checkColour(3, 2), stopAfter=-200, whiteblack=False, pid=robot.movement.track2)

    if robot.fire[1] == False or robot.chemical == False:
        if robot.fire[1] == False:
            robot.movement.gyroTillSense(150, lambda: robot.colour["brown_floor"].condition(), override=0, stop=False)
            robot.movement.gyrodegree(1, 50, maximumSpeed=400, minimumSpeed=100, override=0)
            robot.movement.turn(0, 90, oneWheel=2)
            robot.movement.gyrodegree(1, 40, maximumSpeed=400, minimumSpeed=100)
            robot.basic.beep()
            robot.tasks.depositWater()
        elif robot.chemical == False:
            chemical = robot.movement.gyroTillSense(150, lambda: robot.colour["chemical"].condition(robot.basic.sense(3), robot.basic.sense(5)), stopAfter=100)
            if chemical:
                robot.movement.gyrodegree(1, 220, maximumSpeed=400, minimumSpeed=100)
                robot.movement.turn(0, -45, oneWheel=1)
                robot.movement.gyrodegree(-1, -170, maximumSpeed=400, minimumSpeed=20)
                robot.movement.gyrodegree(1, 130, maximumSpeed=400, minimumSpeed=20)
                robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
                robot.movement.gyrodegree(-200, -100, decel=False, stop=False, override=0)
            else:
                print("other")
        robot.movement.gyroTillSense(-160, lambda: not robot.colour["white_floor"].condition(), override=0)
        robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=400, pid=robot.movement.track2)
        robot.motord.run_target(1500, 0)
        robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=250, pid=robot.movement.track2)
    else:
        robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 200, lambda: False, stopAfter=-150-angleAtDetectBrown, whiteblack=False, pid=robot.movement.track2)
        robot.movement.turn(0, -40, oneWheel=2)
        robot.movement.gyrodegree(-1, -300, maximumSpeed=600)
        robot.motord.run_until_stalled(1500)
        robot.movement.gyroTillSense(-300, lambda: robot.basic.sense(6) < 10)
        robot.movement.gyrodegree(1, 70, maximumSpeed=201)
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(1, 200, maximumSpeed=500)
        robot.movement.moveTillStall(1500)
    return robot