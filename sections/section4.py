from functions.robot import Robot


def section4(robot):
    if robot == None:
        return robot
    
    robot.sensor1.reset_angle(robot.neg(0))
    robot.movement.gyrodegree(-300, -20)

    #Detect 7 + 8
    sensor3 = robot.basic.sense(2)
    sensor4 = robot.basic.sense(3)
    sensor5 = robot.basic.sense(4)
    sensor6 = robot.basic.sense(5)
    

    print(sensor3, sensor4, sensor5, sensor6)
    
    if robot.colour["fire"].condition(sensor3) or robot.colour["fire"].condition(sensor4):
        robot.tasks.depositWater()
    elif robot.colour["human"].condition(sensor3, sensor5) or robot.colour["human"].condition(sensor4, sensor6):
        robot.basic.beep()
        if robot.human[0] == 0:
            robot.human[0] = 1
        else:
            robot.human[1] = 1
    elif robot.colour["chemical"].condition(sensor3, sensor5) or robot.colour["chemical"].condition(sensor4, sensor6):
        robot.basic.beep()
        print("Chemical detected")
        # robot.tasks.collectChemical(2 if robot.colour["chemical"].condition(sensor3) else 1, special=2)
    

    robot.movement.gyrodegree(-200, -220, decel=False, stop=False, override=0)
    robot.movement.gyroTillSense(-150, lambda: robot.colour["brown_floor"].condition(), override=0, stop=False)
    robot.movement.gyrodegree(-200, -170, decel=False, stop=False, override=0)

    robot.movement.gyroTillSense(-200, lambda: robot.tasks.checkColour(robot.basic.sense(3), robot.basic.sense(5), 2, 2, special=2), stopAfter=-80, override=0, stop=False)
    robot.movement.gyrodegree(-200, -250, decel=True, minimumSpeed=80, stop=False, override=0)
    robot.movement.gyroTillSense(-80, lambda: (robot.colour["brown_floor"].condition() != True), override=0, stop=False)
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 200, lambda: robot.tasks.checkColour(robot.basic.sense(3), robot.basic.sense(5), 2, 2, ), stopAfter=-150, whiteblack=False)

    robot.movement.gyroTillSense(150, lambda: robot.colour["brown_floor"].condition(), override=0, stop=False)
    robot.movement.gyrodegree(200, 320, decelDist=300)
    robot.pause(0.5)
    robot.movement.turn(0, -90, oneWheel=2)
    robot.moveTillStall(1500)

    return robot