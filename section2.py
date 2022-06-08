from movements import Robot
import time

def section2(robot):
    if robot == None:
        return robot
    
    #Reset Angle
    robot.sensor1.reset_angle(int(robot.startingPos) * 90)

    #Do for plan a (Move front more)
    # robot.pidmovegyrodegree(-160, -700)
    robot.pidmovegyrodegree(-15*int(robot.startingPos)-145, -700)
    robot.pidturn(0, robot.sensorVal(0), oneWheel=-0.5*int(robot.startingPos)+1.5)

    #Line tracking
    #Do for plan a (Brown instead of blue)
    def condition1():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] < 10 and robot.sensorVal(1)[1] < 30 and robot.sensorVal(1)[2] > 30)
        elif int(robot.startingPos) == -1:
            return (robot.sensorVal(1)[0] > 15 and robot.sensorVal(1)[1] < 15 and robot.sensorVal(1)[2] < 15)
    condition1 = condition1
    robot.lineTrackingTillSense(12, 300, condition1)

    print(robot.sensorVal(0))
    print(int(robot.startingPos)*180 - robot.sensorVal(0))
    robot.pidturn(0, int(robot.startingPos)*180 - robot.sensorVal(0))

    #Detect 1
    def checkCondition():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] < 40)
        elif int(robot.startingPos) == -1:
            #Change
            return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    condition=checkCondition
    detected = robot.gyroForwardTillSense(200, 2, 70, leeway1=400, leeway2=0, stopAfter=-300, override=int(robot.startingPos)*180, backwards=True)
    if detected != None:
        print("detected")
        robot.checkColour(detected, 1, 6)
    robot.beep()
    
    #Move forward
    def condition1():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 15 or robot.sensorVal(1)[1] < 30 or robot.sensorVal(1)[2] > 20)
        elif int(robot.startingPos) == -1:
            return (robot.sensorVal(1)[0] < 40 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] > 20)
    condition1 = condition1
    robot.gyroForwardTillSense(-400, 1, 0, condition=condition1, override=int(robot.startingPos)*180)


    #Detect 2
    def checkCondition():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] < 40)
        elif int(robot.startingPos) == -1:
            #Change
            return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    condition=checkCondition
    detected = robot.gyroForwardTillSense(300, 2, 70, leeway1=400, leeway2=0, stopAfter=-150, override=int(robot.startingPos)*180, backwards=True)
    if detected != None:
        element = robot.checkColour(detected, 1, 6)
            
    robot.beep()
    robot.pidmovegyrodegree(-50, -700)

    #Detect 3
    if int(robot.startingPos) == 1:
        def checkCondition():
            if int(robot.startingPos) == 1:
                return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] < 40)
            elif int(robot.startingPos) == -1:
                #Change
                return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
        condition=checkCondition
        detected = robot.gyroForwardTillSense(300, 2, 70, leeway1=400, leeway2=0, stopAfter=-150, override=int(robot.startingPos)*180, backwards=True)
        if detected != None:
            robot.checkColour(detected, 1, 5)
        robot.beep()
    elif int(robot.startingPos) == -1:
        robot.pidmovegyrodegree(-150, -700)

    #Correction
    robot.pidturn(0, 160)
    robot.move(1500, 1500)
    time.sleep(1)
    robot.stop()
    robot.sensor1.reset_angle(0)
    robot.pidmovegyrodegree(-180, -700)
    robot.pidturn(0, 90, oneWheel=1)
    robot.move(1500, 1500)
    time.sleep(1)
    robot.stop()
    robot.sensor1.reset_angle(90)
    robot.pidmovegyrodegree(-30, -700)

    def checkCondition():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] < 40)
        elif int(robot.startingPos) == -1:
            #Change
            return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    condition=checkCondition
    detected = robot.gyroForwardTillSense(300, 2, 70, leeway1=400, leeway2=0, stopAfter=-150, override=int(robot.startingPos)*180, backwards=True)
    if detected != None:
        element = robot.checkColour(detected, 1, 6)
            
    robot.beep()
    robot.pidmovegyrodegree(-400, -700)
    

    def checkCondition():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] < 40)
        elif int(robot.startingPos) == -1:
            #Change
            return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    condition=checkCondition
    detected = robot.gyroForwardTillSense(300, 2, 70, leeway1=400, leeway2=0, stopAfter=-150, override=int(robot.startingPos)*180, backwards=True)
    if detected != None:
        element = robot.checkColour(detected, 1, 6)
            
    robot.beep()
    robot.pidmovegyrodegree(-400, -700)

    def checkCondition():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] < 40)
        elif int(robot.startingPos) == -1:
            #Change
            return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    condition=checkCondition
    detected = robot.gyroForwardTillSense(300, 2, 70, leeway1=400, leeway2=0, stopAfter=-150, override=int(robot.startingPos)*180, backwards=True)
    if detected != None:
        element = robot.checkColour(detected, 1, 6)
            
    robot.beep()
    robot.pidmovegyrodegree(-400, -700)
    

    # print("Angle 1:", robot.sensorVal(0))
    # if detected != None:
    #     robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    # robot.pidmovegyrodegree(400, 500)
    # detected = robot.gyroForwardTillSense(-300, 4, 40, stopAfter=100, leeway1=400, leeway2=0, override=0)
    # print("Angle 2:", robot.sensorVal(0))
    # if detected != None:
    #     robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    # def checkCondition():
    #     if int(robot.startingPos) == 1:
    #         return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] < 40 or robot.sensorVal(1)[2] > 20)
    #     elif int(robot.startingPos) == -1:
    #         #Change
    #         return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    # condition=checkCondition
    # detected = robot.gyroForwardTillSense(300, 3, 40, leeway1=400, leeway2=0, condition=condition)
    # if detected != None:
    #     robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    
    # #change stop after if needed
    # detected = robot.gyroForwardTillSense(300, 3, 15, stopAfter=400, leeway1=400, leeway2=0)
    # if detected != None:
    #     #Check color
    #     print()
    # if robot.startingPos == 1:
    #     detected = robot.gyroForwardTillSense(300, 3, 15, stopAfter=400, leeway1=400, leeway2=0)
    #     if detected != None:
    #         #Check color
    #         print()
    # robot.pidmovegyrodegree(100, 500)
    # if robot.startingPos == -1:
    #     robot.pidturn(150, -45)
    #     #change values
    #     robot.pidmovegyrodegree(100, 500)
    #     robot.pidturn(150, 45)
    #     robot.move(1500, 1500)
    #     time.sleep(1.5)
    #     robot.sensor1.reset_angle(0)
    return robot