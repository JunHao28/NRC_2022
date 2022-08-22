def section4(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.neg(90))
    robot.movement.gyrodegree(-300, -50)

    #Detect 7 + 8
    sensor3 = robot.basic.sense(2)
    sensor4 = robot.basic.sense(3)
    if robot.colour["chemical"].condition(sensor3) or robot.colour["chemical"].condition(sensor4):
        robot.collectChemical(2 if robot.colour["chemical"].condition(sensor3) else 1, special=2)
    elif robot.colour["fire"].condition(sensor3) or robot.colour["fire"].condition(sensor4):
        robot.depositWater()
    elif robot.colour["human"].condition(sensor3) or robot.colour["human"].condition(sensor4):
        if robot.human[0] == 0:
            robot.human[0] = 1
        else:
            robot.human[1] = 1

    robot.movement.gyrodegree(-300, -60)
    robot.movement.gyrodegree(-300, -120, decel=False, stop=False)
    robot.movement.gyroTillSense(-80, lambda: robot.colour["brown_floor"].condition(), override=robot.neg(90), stop=False)
    robot.movement.gyrodegree(-300, -170, decel=False, stop=False)

    robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(robot.basic.sense(3), 2, 2, special=2), stopAfter=-80, override=robot.neg(90), stop=False)
    robot.movement.gyrodegree(-300, -120, decel=False, stop=False)
    robot.movement.gyroTillSense(-80, lambda: (robot.colour["brown_floor"].condition() != True), override=robot.neg(90), stop=False)
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"])