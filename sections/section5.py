from functions.robot import Robot

from random import randint

def section5(robot):
    if robot == None:
        return robot

    arrangeList=robot.side([2, 1, 4, 3, 6, 5], [6, 5, 4, 3, 2, 1])

    human = []
    # if human[0] == 0:
    #     human[0] = randint(1, 6)
    if robot.human[1] == 0:
        robot.human[1] = 4
    human.append(arrangeList.index(robot.human[0]))
    human.append(arrangeList.index(robot.human[1]))
    human.sort()

    robot.sensor1.reset_angle(-90)
    robot.movement.turn(0, -180 - robot.basic.sense(0), oneWheel=2)
    robot.motord.run_angle(1500, -300)
    robot.movement.decelerate(900)

    robot.movement.turn(0, -180 - robot.basic.sense(0), oneWheel=0)
    robot.movement.moveTillStall(1000)
    robot.sensor1.reset_angle(-180)
    robot.tasks.depositYellow()
    robot.movement.gyrodegree(-300, -95, decel=False, override=-180)
    robot.movement.turn(0, -90 - robot.basic.sense(0), oneWheel=1)
    robot.movement.gyroTillSense(-100, lambda: robot.sensor2.reflection() > 30)
    robot.tasks.collectYellow()
    if human[0] == 0: #Brown, Blue
        robot.movement.turn(0, 90, oneWheel=1)
        robot.movement.gyrodegree(-10, -80, decel=False, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 70, decel=False, times=False)
        robot.movement.turn(0, -90, oneWheel=1)
        robot.movement.gyrodegree(-80, -100)
    elif human[0] == 1: #Red, Green
        robot.movement.gyrodegree(80, 40, decel=False)
        robot.motorb.run_angle(800, -220)
        robot.tasks.depositYellow()
        robot.motorb.run_angle(800, 220)
        robot.movement.gyrodegree(-80, -180, decel=False, override=-90)
    elif human[0] == 2: #White
        robot.movement.gyrodegree(-300, -150, decel=False)
        robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(-10, -80, decel=False, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 60, decel=False, times=False)
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    elif human[0] == 3: #Yellow
        robot.movement.gyrodegree(-300, -100, decel=False, override=-90)
        robot.motorb.run_angle(800, -220)
        robot.tasks.depositYellow()
        robot.motorb.run_angle(800, 220)
    elif human[0] == 4: #Blue, Brown
        robot.motorb.run_angle(800, -110)
        robot.movement.gyrodegree(-100, -300, decel=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(100, 300, decel=False)
        robot.motorb.run_angle(800, 110)
        robot.movement.gyrodegree(-80, -180, decel=False, override=-90)

    robot.movement.gyroTillSense(-80, lambda: robot.sensor2.reflection() > 29, override=-90)
    robot.tasks.collectYellow()
    if human[1] == 4:
        robot.movement.turn(0, 90, oneWheel=1)
        robot.movement.gyrodegree(-10, -80, decel=False, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 60, decel=False, times=False)
        robot.movement.turn(0, -90, oneWheel=1)
    elif human[1] == 5:
        robot.movement.gyrodegree(80, 40, decel=False)
        robot.pause(0.5)
        robot.movement.turn(0, 65, oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90 - robot.basic.sense(0), oneWheel=1)
    elif human[1] == 3:
        robot.movement.gyrodegree(300, 150, decel=False)
        robot.movement.turn(0, -robot.basic.sense(0), oneWheel=1)
        robot.movement.gyrodegree(-10, -80, decel=False, times=False)
        robot.tasks.depositYellow()
        robot.movement.gyrodegree(10, 60, decel=False, times=False)
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    elif human[1] == 2:
        robot.movement.gyrodegree(300, 150, decel=False)
        robot.pause(0.5)
        robot.movement.turn(0, -30 - robot.basic.sense(0), oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    elif human[1] == 1:
        robot.movement.gyrodegree(300, 280, decel=False)
        robot.pause(0.5)
        robot.movement.turn(0, -20-robot.basic.sense(0), oneWheel=1)
        robot.tasks.depositYellow()
        robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=1)
    
    robot.movement.moveTillStall(700)
    robot.pause(0.2)
    robot.sensor1.reset_angle(-180)
    
    robot.motord.run_angle(1500, -300)
    robot.movement.turn(0, -75, oneWheel=2)
    robot.movement.moveTillStall(1000)
    return robot



# def section5(robot):
#     if robot == None:
#         return robot

#     robot.sensor1.reset_angle(-90)
#     robot.movement.gyrodegree(-200, -200, decel=False, stop=False, override=-90)
#     robot.movement.gyroTillSense(-16, lambda: robot.colour["white_floor"].condition(), override=-90, stop=False)
#     robot.movement.gyrodegree(-1, -370, startingSpeed=160, maximumSpeed=500, override=-90)
#     robot.basic.stop()
#     robot.movement.turn(0, -robot.basic.sense(0), oneWheel=robot.side(2, 0))
#     robot.pause(0.5)
#     robot.movement.gyroTillSense(-300, lambda: robot.tasks.checkColour(2, 2, special=2), stopAfter=-80, override=0, stop=True)
#     robot.tasks.reset()
    
#     robot.movement.gyrodegree(-200, -220, maximumSpeed=500, minimumSpeed=160, stop=False, override=0)
#     robot.movement.gyroTillSense(-160, lambda: (not robot.colour["white_floor"].condition()), override=0, stop=False)
#     robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 150, lambda: robot.tasks.checkColour(3, 2), stopAfter=200, pid=robot.movement.track2)
#     robot.tasks.reset()
#     robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=250, pid=robot.movement.track2)
#     robot.motord.run_target(1500, 0)
#     robot.movement.lineTrackingTillSense(robot.colour["line_tracking_2"], 300, lambda: False, stopAfter=100, pid=robot.movement.track2)
#     robot.movement.gyrodegree(-300, -100, override=0)
#     robot.movement.turn(0, -90, oneWheel=1)
#     robot.movement.gyrodegree(300, 400)
#     robot.movement.moveTillStall(1500)
#     robot.sensor1.reset_angle(-90)
#     robot.movement.gyrodegree(-200, -10)
#     robot.movement.turn(0, -90, oneWheel=2)
    
#     robot.movement.turn(0, -90-robot.basic.sense(0), oneWheel=2)
#     robot.movement.moveTillStall(1500)
#     return robot