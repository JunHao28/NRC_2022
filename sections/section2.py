from functions.robot import Robot
import time

def section2(robot):
    if robot == None:
        return robot
    
    #Reset Angle
    robot.sensor1.reset_angle(int(robot.startingPos) * 90)

    #Do for plan a (Move front more)
    robot.gyrodegree(-700, -160)
    # robot.gyrodegree(-15*int(robot.startingPos)-145, -700)
    robot.turn(0, robot.sense(0), oneWheel=-0.5*int(robot.startingPos)+1.5)

    #Line tracking
    robot.lineTrackingTillSense(12, 400, robot.colour.check(robot.colour.blue_floor if int(robot.startingPos) == 1 else robot.colour.brown_floor))

    #Face 0°
    robot.turn(0, int(robot.startingPos)*180 - robot.sense(0))

    #Detect 1
    robot.gyroTillSense(-300, lambda: robot.checkColour(robot.sense(2), 1, 2.5*int(robot.startingPos)+3.5), stopAfter=-200, override=int(robot.startingPos)*180)
    
    #Move forward
    robot.gyrodegree(-1000, -300)
    robot.gyroTillSense(-300, lambda: robot.colour.check(robot.colour.green_floor if int(robot.startingPos) == 1 else robot.colour.red_floor), override=int(robot.startingPos)*180)
    angleAtDetectGreen = robot.motorb.angle()
    robot.gyrodegree(-700, -150)

    #Detect 2
    robot.gyroTillSense(300, lambda: robot.checkColour(robot.sense(2), 1, 2.5*int(robot.startingPos)+3.5, special=True), stopAfter=-200, override=int(robot.startingPos)*180)    

    #Move Forward
    robot.gyrodegree(-700, -30)

    #Detect 3
    if int(robot.startingPos) == 1:
        robot.gyroTillSense(300, lambda: robot.checkColour(robot.sense(2), 1, 5, special=True), stopAfter=-150, override=int(robot.startingPos)*180, backwards=True)

    robot.gyro(300, condition=lambda: return (robot.motorb.angle() - angleAtDetectGreen < 200))

    
        

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