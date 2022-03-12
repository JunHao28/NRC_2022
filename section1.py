from movements import Robot

def section1(robot):
    print("true")
    if sum(robot.sensorVal(1)) > 40:
        robot.startingPos = StartingPos.left
    elif sum(robot.sensorVal(2)) > 40:
        robot.startingPos = StartingPos.right
    else: 
        return None
    return robot