from functions.movements import Movement
from functions.basic import Basic
from functions.tasks import Tasks


class Robot:

    startingPos = None
    human = [0, 0]
    chemical = False

    def __init__(self, ev3, motor, sensor, wait):
        self.ev3 = ev3
        self.motorb = motor[0]
        self.motorc = motor[1]
        self.motord = motor[2]
        self.sensor1 = sensor[0]
        self.sensor2 = sensor[1]
        self.sensor3 = sensor[2]
        self.sensor4 = sensor[3]
        self.stop = wait

        basic = Basic(ev3, motor, sensor)
        self.basic = basic
        self.colour = {
            "red_floor": Colour("red_floor", lambda: (basic.sense(1)[0] < 40 or basic.sense(1)[1] > 20 or basic.sense(1)[2] > 20)),
            "brown_floor": Colour("brown_floor", lambda: (basic.sense(1)[0] > 15 and basic.sense(1)[1] < 15 and basic.sense(1)[2] < 15)), #Not done yet
            "yellow_floor": Colour("yello_floor", lambda: (basic.sense(1)[0] > 60 and basic.sense(1)[1] > 40 and basic.sense(1)[2] < 30)),
            "blue_floor": Colour("blue_floor", lambda: (basic.sense(1)[0] < 15 and basic.sense(1)[1] < 30 and basic.sense(1)[2] > 40)),
            "green_floor": Colour("green_floor", lambda: (basic.sense(1)[0] < 15 and basic.sense(1)[1] > 30 and basic.sense(1)[2] < 20)),
            
            # "chemical": Colour("chemical", lambda val: val[2] > 10 and sum(val) > 30 and val[0] - val[1] <= 7 and val[0] - val[1] >= -7 and val[1] - val[2] <= 7 and val[1] - val[2] >= -7),
            "chemical": Colour("chemical", lambda val: val[0] > 11 and val[0] < 19 and val[1] > 18 and val[1] < 24 and val[2] > 12 and val[2] < 18 and val[3] > 44 and val[3] < 48),
            "fire": Colour("fire", lambda val: val[0] >= 50 and val[1] <= 50 and val[2] <= 50),
            "human": Colour("human", lambda val: sum(val) > 250),
            "line_tracking": 37
        }
        self.movement = Movement(ev3, motor, sensor, self.basic)
        self.tasks = Tasks(ev3, motor, sensor, self.colour, self.basic, self.human, self.chemical, self.movement, lambda time: self.pause(time))

    def pause(self, seconds):
        self.stop(seconds*1000)

    def neg(self, number):
        return int(self.startingPos) * number

    def side(self, right, left):
        if int(self.startingPos) == 1:
            return right
        elif int(self.startingPos) == -1:
            return left

    

class Colour:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition