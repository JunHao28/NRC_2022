from functions.movements import Movement
from functions.unchanged.ColorCheck import Colours
from functions.basic import Basic
from functions.tasks import Tasks


class Robot:

    startingPos = None
    human = [0, 0]

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


        self.basic = Basic(ev3, motor, sensor)
        self.colour = Colours(self.basic)
        self.movement = Movement(ev3, motor, sensor, self.basic)
        self.tasks = Tasks(ev3, motor, sensor, self.colour, self.basic, self.human, self.movement, lambda: self.wait())

    def pause(self, seconds):
        self.stop(seconds*1000)

    def neg(self, number):
        return int(self.startingPos) * number

    def side(self, right, left):
        if int(self.startingPos) == -1:
            return right
        elif int(self.startingPos) == 1:
            return left

    
