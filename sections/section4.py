from functions.robot import Robot


def section4(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.neg(0))

    #Detect 7 + 8
    robot.print("7+8:")
    condition = lambda: robot.side((robot.tasks.checkColour(3, 1, special=2) or robot.tasks.checkColour(2, 1, special=2)), (robot.tasks.checkColour(3, 1, special=2)), )
    robot.movement.gyroTillSense(-200, condition, stopAfter=-50, override=0)
    robot.tasks.reset()

    robot.basic.beep()
    robot.movement.gyrodegree(-1, -170, maximumSpeed=400, minimumSpeed=150, stop=False, override=0)
    
    robot.movement.turn(0, -robot.basic.sense(0))
    robot.motorb.run_angle(300, -70)
    robot.motorc.run_angle(300, -70)
    robot.movement.turn(0, -robot.basic.sense(0))
    
    robot.movement.gyroTillSense(-140, lambda: robot.colour[robot.side("brown_floor", "blue_floor")].condition(), override=0, stop=False)
    robot.movement.gyrodegree(-1, robot.side(-180, -100), startingSpeed=150, maximumSpeed=400, minimumSpeed=250, stop=False, override=0)

    robot.basic.beep()

    #Detect 9
    robot.print("9:")
    if robot.side(False, True):
        robot.movement.gyroTillSense(-200, lambda: robot.tasks.checkColour(1, 2, special=1), stopAfter=-80, override=0, stop=False)
        robot.tasks.reset()
        robot.movement.gyrodegree(-1, -30, stop=False, override=180, accelDist=1, maximumSpeed=201)
    
    #Detect 10
    robot.print("10:")
    robot.movement.gyroTillSense(-200, lambda: robot.tasks.checkColour(3, 2, special=robot.side(2, 1)), stopAfter=-80, override=0, stop=False)
    robot.tasks.reset()


    robot.movement.gyrodegree(-1, -200, maximumSpeed=500, minimumSpeed=80, stop=False, override=0)
    robot.movement.gyroTillSense(-160, lambda: (not robot.colour[robot.side("brown_floor", "blue_floor")].condition()), override=0, stop=False)
    angleAtDetectBrown = robot.motorb.angle()

    #Detect 11
    robot.print("11:")
    robot.movement.gyroTillSense(-250, lambda: robot.tasks.checkColour(3, 2), stopAfter=-200, override=0)
    if robot.fire[1] == False or robot.tasks.returnchem() == False:
        robot.movement.gyroTillSense(150, lambda: robot.colour[robot.side("brown_floor", "blue_floor")].condition(), override=0, stop=False)
        robot.movement.gyrodegree(1, 55, maximumSpeed=400, minimumSpeed=100, override=0)
        robot.movement.turn(0, robot.neg(90), oneWheel=robot.side(2, 1))
        robot.movement.gyrodegree(1, 50, maximumSpeed=400, minimumSpeed=100)
        if robot.fire[1] == False:
            robot.basic.beep()
            robot.tasks.depositWater()
            robot.movement.gyrodegree(1, 220, maximumSpeed=400, minimumSpeed=100)
            robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
            robot.movement.gyrodegree(-200, -100, decel=False, stop=False, override=0)
        elif robot.tasks.returnchem() == False:
            chemical = robot.movement.gyroTillSense(200, lambda: robot.colour["chemical"].condition(robot.basic.sense(3), robot.basic.sense(5)), stopAfter=100)
            if chemical:
                robot.movement.gyrodegree(robot.neg(1), robot.neg(220), maximumSpeed=400, minimumSpeed=100)
                robot.movement.turn(0, robot.neg(-45), oneWheel=1)
                robot.movement.gyrodegree(-1, -170, maximumSpeed=400, minimumSpeed=20)
                robot.motord.run_target(1500, -200)
                robot.movement.gyrodegree(1, 130, maximumSpeed=400, minimumSpeed=20)
                robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
                robot.movement.gyrodegree(-200, -100, decel=False, stop=False, override=0)
            else:
                robot.movement.gyrodegree(1, 400, maximumSpeed=600, minimumSpeed=100)
                robot.movement.turn(0, 45, oneWheel=1)
                robot.movement.gyrodegree(-1, -252, maximumSpeed=400, minimumSpeed=20)
                robot.motord.run_target(1500, -200)
                robot.movement.gyrodegree(1, 330, maximumSpeed=400, minimumSpeed=20)
                robot.movement.turn(0, -robot.basic.sense(0), oneWheel=2)
                robot.movement.gyrodegree(-200, -100, decel=False, stop=False, override=0)
        white = robot.basic.sense(1)
        robot.movement.gyroTillSense(-160, lambda: sum(white) - sum(robot.basic.sense(1)) > 17, override=0)
        robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=400, pid=robot.movement.track2)
        robot.motord.run_target(1500, 0)
        robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=260, pid=robot.movement.track2)
        robot.movement.turn(0, -90, oneWheel=1)
        robot.movement.gyrodegree(300, 400)
        robot.movement.moveTillStall(1500)
        robot.sensor1.reset_angle(-90)
    else:
        robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 200, lambda: False, stopAfter=abs(-150-angleAtDetectBrown), whiteblack=False, pid=robot.movement.track2)
        robot.movement.turn(0, -40, oneWheel=2)
        robot.movement.gyrodegree(-1, -300, maximumSpeed=600)
        robot.motord.run_until_stalled(1500)
        robot.movement.gyroTillSense(-400, lambda: robot.basic.sense(6) < 10)
        robot.movement.gyrodegree(1, 70, maximumSpeed=201)
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(1, 200, maximumSpeed=500)
        robot.movement.moveTillStall(1500)
    return robot