from movements import Robot
import time

def section2(robot):
    if robot == None:
        return robot
    #Do for plan a
    robot.pidmovegyrodegree(-160, -700)  
    robot.pidturn(0, int(robot.startingPos) * -180 + robot.sensorVal(0), oneWheel=2)
    print("Angle after turn:", robot.sensorVal(0))
    time.sleep(0.1)
    def checkCondition():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] > 20 or robot.sensorVal(1)[2] < 40)
        elif int(robot.startingPos) == -1:
            #Change
            return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    condition=checkCondition
    detected = robot.gyroForwardTillSense(300, 3, 40, leeway1=400, leeway2=0, condition=condition, override=0)
    print("Angle 1:", robot.sensorVal(0))
    if detected != None:
        robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    robot.pidmovegyrodegree(400, 500)
    detected = robot.gyroForwardTillSense(300, 3, 40, stopAfter=100, leeway1=400, leeway2=0, override=0)
    print("Angle 2:", robot.sensorVal(0))
    if detected != None:
        robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    def checkCondition():
        if int(robot.startingPos) == 1:
            return (robot.sensorVal(1)[0] > 20 or robot.sensorVal(1)[1] < 40 or robot.sensorVal(1)[2] > 20)
        elif int(robot.startingPos) == -1:
            #Change
            return (robot.sensorVal(1)[0] > 60 or robot.sensorVal(1)[1] > 60 or robot.sensorVal(1)[2] < 60)
    condition=checkCondition
    detected = robot.gyroForwardTillSense(300, 3, 40, leeway1=400, leeway2=0, condition=condition)
    if detected != None:
        robot.checkColour(detected, 2, (2.5*int(robot.startingPos)+3.5))
    
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