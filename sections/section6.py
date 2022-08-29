from functions.robot import Robot

def section6(robot):
    if robot == None:
        return robot
    
    # robot.human = [1,2]
    arrangeList=[2, 1, 4, 3, 6, 5]
    human = []
    human.append(arrangeList.index(robot.human[0]))
    human.append(arrangeList.index(robot.human[1]))
    human.sort()
    print(human)

    robot.sensor1.reset_angle(-90)
    robot.movement.turn(0, -180 - robot.basic.sense(0), oneWheel=2)
    robot.movement.moveTillStall(1500)
    robot.pause(0.2)
    robot.sensor1.reset_angle(-180)
    robot.tasks.depositYellow()
    robot.movement.gyrodegree(-300, -80)
    robot.movement.turn(0, -90 - robot.basic.sense(0), oneWheel=1)
    robot.movement.gyroTillSense(-100, lambda: False, stopAfter=-50)
    robot.tasks.collectYellow()
    angleAtCollect = robot.motorb.angle()
    if human[0] == 0:
        robot.movement.turn(0, 90, oneWheel=1)
        robot.movement.gyrodegree(-10, -80, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 70, times=False)
        robot.movement.turn(0, -90, oneWheel=1)
        robot.movement.gyrodegree(-80, -100)
    elif human[0] == 1:
        robot.movement.gyrodegree(80, 40)
        robot.pause(0.5)
        robot.movement.turn(0, 65, oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90 - robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(-80, -180, override=-90)
    elif human[0] == 2:
        robot.movement.gyrodegree(-300, -150)
        robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(-10, -80, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 60, times=False)
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    elif human[0] == 3:
        robot.movement.gyrodegree(-300, -150)
        robot.movement.turn(0, -30 - robot.basic.sense(0), oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    elif human[0] == 4:
        robot.movement.gyrodegree(-300, -150)
        robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(-10, -20, times=False)
        robot.movement.turn(0, -70-robot.basic.sense(0), oneWheel=2)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(-10, -20, times=False)
        robot.movement.gyrodegree(10, 20, times=False)
        robot.movement.turn(0, -robot.basic.sense(0), oneWheel=2)
        robot.movement.gyrodegree(10, 10, times=False)
        robot.movement.gyrodegree(300, 150)
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    # robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 150, lambda: robot.sensor2.reflection() > 30, pid=robot.movement.track2)
    robot.movement.gyroTillSense(-80, lambda: robot.sensor2.reflection() > 29)
    robot.tasks.collectYellow()
    if human[1] == 4:
        robot.movement.turn(0, 90, oneWheel=1)
        robot.movement.gyrodegree(-10, -80, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 70, times=False)
        robot.movement.turn(0, -90, oneWheel=1)
    elif human[1] == 5:
        robot.movement.gyrodegree(80, 40)
        robot.pause(0.5)
        robot.movement.turn(0, 65, oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90 - robot.basic.sense(0), oneWheel=1)
    elif human[1] == 3:
        robot.movement.gyrodegree(300, 150)
        robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(-10, -80, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 60, times=False)
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    elif human[1] == 2:
        robot.movement.gyrodegree(300, 150)
        robot.pause(0.5)
        robot.movement.turn(0, -30 - robot.basic.sense(0), oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    elif human[1] == 1:
        robot.movement.gyrodegree(300, 280)
        robot.pause(0.5)
        robot.movement.turn(0, -20-robot.basic.sense(0), oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    robot.basic.move(700, 700)
    robot.pause(1)
    robot.basic.stop()
    robot.pause(0.2)
    robot.sensor1.reset_angle(-180)
    robot.movement.turn(0, -80, oneWheel=2)
    robot.movement.moveTillStall(1500)
    return robot