from movements import Robot
import time

def section2(robot):
    detected = robot.gyroForwardTillSense(300, 3, 15, stopAfter=400, leeway1=400, leeway2=0)
    if detected != None:
        #Check color
        print(detected)
    # robot.pidmovegyrodegree(200, 500)
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