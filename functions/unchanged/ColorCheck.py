class Colour:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

class Colours:

    blue_floor = Colour(blue_floor, lambda: return (robot.sense(1)[0] < 10 and robot.sense(1)[1] < 30 and robot.sense(1)[2] > 30))
    brown_floor = Colour(brown_floor, lambda: return (robot.sense(1)[0] > 15 and robot.sense(1)[1] < 15 and robot.sense(1)[2] < 15))
    green_floor = Colour(green_floor, lambda: return (robot.sense(1)[0] > 15 or robot.sense(1)[1] < 30 or robot.sense(1)[2] > 20))
    red_floor = Colour(red_floor, lambda: return (robot.sense(1)[0] < 40 or robot.sense(1)[1] > 20 or robot.sense(1)[2] > 20))

    def check(self, name):
        return name.conditon()
