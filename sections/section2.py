from functions.robot import Robot
import time

def section2(robot):
    if robot == None:
        return robot
    
    #Reset Angle
    robot.sensor1.reset_angle(robot.neg(90))

    robot.movement.gyrodegree(-100, robot.side(-155, -160), maximumSpeed=300, decel=False)
    robot.pause(0.5)
    robot.movement.turn(0, robot.neg(robot.basic.sense(0)), oneWheel=robot.side(2, 1))
    
    #Line tracking
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"], 300, lambda: robot.colour[robot.side("blue_floor", "brown_floor")].condition())

    #Face 180°
    robot.movement.turn(0, robot.neg(180) - robot.basic.sense(0))
    # robot.motorb.run_angle(300, -100)
    # robot.motorc.run_angle(300, -100)
    # robot.movement.turn(0, -15, oneWheel=2)

    #Detect 1
    robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(robot.basic.sense(2), 2, robot.side(6, 2)), stopAfter=-250, override=180, stop=False)
    # robot.ev3.speaker.say("one")

    #Move forward
    robot.movement.gyrodegree(-300, -180, decel=False, stop=False)
    robot.movement.gyroTillSense(-80, lambda: robot.colour[robot.side("green_floor", "red_floor")].condition(), override=robot.neg(180), stop=False)
    angleAtDetectGreen = robot.motorb.angle()
    # robot.movement.gyrodegree(-700, -100)
    # robot.basic.beep()

    #Detect 2
    robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(robot.basic.sense(2), 2, robot.side(6, 2), special=1), stopAfter=-140, override=robot.neg(180), stop=False)

    #Move Forward
    robot.movement.gyrodegree(-300, -30, decel=False, stop=False)
    # robot.basic.beep()

    #Detect 3
    if int(robot.startingPos) == 1:
        robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(robot.basic.sense(2), 2, 5, special=1), stopAfter=-60, override=robot.neg(180), stop=False)
        robot.movement.gyrodegree(-20, -270 - (robot.motorb.angle() - angleAtDetectGreen))
    robot.movement.turn(0, robot.side(-90, 180), oneWheel=robot.side(2, 0))
    robot.basic.move(1500, 1500)
    robot.pause(1)
    robot.movement.stop()
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
    robot.movement.stop()
    robot.sensor1.reset_angle(robot.neg(90))
    robot.movement.gyrodegree(-300, -50)

    #Detect 7 + 8
    sensor3 = robot.basic.sense(2)
    sensor4 = robot.basic.sense(3)
    if robot.colour["chemical"].condition(sensor3) or robot.colour["chemical"].condition(sensor4):
        robot.collectChemical(2 if robot.colour["chemical"].condition(sensor3) else 1, special=2)
    elif robot.colour["fire"].condition(sensor3) or self.colour["fire"].condition(sensor4):
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

    robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(robot.basic.sense(3), 2, 2), special=2), stopAfter=-80, override=robot.neg(90), stop=False)
    robot.movement.gyrodegree(-300, -120, decel=False, stop=False)
    robot.movement.gyroTillSense(-80, lambda: (robot.colour["brown_floor"].condition() != True), override=robot.neg(90), stop=False)
    robot.movement.lineTrackingTillSense(robot.colour["line_tracking"])



    
        

    #Correction
    # robot.turn(0, -10*int(robot.startingPos)+160) #160 for RIGHT 180 for LEFT
    # robot.move(1500, 1500)
    # time.sleep(1)
    # robot.stop()
    # robot.sensor1.reset_angle(0)
    # robot.gyrodegree(-700, -180)
    # robot.turn(0, 90, oneWheel=1)
    # robot.move(1500, 1500)
    # time.sleep(1)
    # robot.stop()
    # robot.sensor1.reset_angle(int(robot.startingPos)*90)
    # robot.gyrodegree(-700, -30)

    # def checkCondition():
    #     robot.checkColour(robot.sense(2), 1, 6)
    # condition=checkCondition
    # detected = robot.gyroTillSense(300, 2, -1, leeway1=0, leeway2=0, condition=condition, stopAfter=-80, override=90, backwards=True)
            
    # robot.beep()
    # robot.gyrodegree(-700, -230)
    # robot.beep()


    # def checkCondition():
    #     robot.checkColour(robot.sense(2), 1, 6)
    # condition=checkCondition
    # detected = robot.gyroTillSense(300, 2, -1, leeway1=0, leeway2=0, condition=condition, stopAfter=-150, override=90, backwards=True)

            
    # robot.beep()
    # def condition1():
    #     if int(robot.startingPos) == 1:
    #         return (robot.sense(1)[0] < 30 or robot.sense(1)[1] > 30 or robot.sense(1)[2] > 30)
    # condition1 = condition1
    # robot.gyroTillSense(-400, 1, 0, condition=condition1, override=-90)
    # time.sleep(0.1)
    # robot.turn(0, -15, oneWheel=2)
    # time.sleep(0.1)
    # robot.gyrodegree(-700, -230)
    # robot.turn(0, -robot.sense(0), oneWheel=1)
    # robot.move(1500, 1500)
    # time.sleep(1)
    # robot.stop()
    # robot.gyrodegree(-700, -30)

    
    

    # print("Angle 1:", robot.sense(0))
    # if detected != None:
    #     robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    # robot.gyrodegree(500, 400)
    # detected = robot.gyroTillSense(-300, 4, 40, stopAfter=100, leeway1=400, leeway2=0, override=0)
    # print("Angle 2:", robot.sense(0))
    # if detected != None:
    #     robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    # def checkCondition():
    #     if int(robot.startingPos) == 1:
    #         return (robot.sense(1)[0] > 20 or robot.sense(1)[1] < 40 or robot.sense(1)[2] > 20)
    #     elif int(robot.startingPos) == -1:
    #         #Change
    #         return (robot.sense(1)[0] > 60 or robot.sense(1)[1] > 60 or robot.sense(1)[2] < 60)
    # condition=checkCondition
    # detected = robot.gyroTillSense(300, 3, 40, leeway1=400, leeway2=0, condition=condition)
    # if detected != None:
    #     robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    
    # #change stop after if needed
    # detected = robot.gyroTillSense(300, 3, 15, stopAfter=400, leeway1=400, leeway2=0)
    # if detected != None:
    #     #Check color
    #     print()
    # if robot.startingPos == 1:
    #     detected = robot.gyroTillSense(300, 3, 15, stopAfter=400, leeway1=400, leeway2=0)
    #     if detected != None:
    #         #Check color
    #         print()
    # robot.gyrodegree(500, 100)
    # if robot.startingPos == -1:
    #     robot.turn(150, -45)
    #     #change values
    #     robot.gyrodegree(500, 100)
    #     robot.turn(150, 45)
    #     robot.move(1500, 1500)
    #     time.sleep(1.5)
    #     robot.sensor1.reset_angle(0)
    return robot