from functions.movements import Movement
from functions.unchanged.ColorCheck import ColorCheck

class Robot:

    startingPos = None
    human = [0, 0]
    colour = ColorCheck()

    def __init__(self, ev3, motor, sensor):
        self.ev3 = ev3
        self.motorb = motor[0]
        self.motorc = motor[1]
        self.motord = motor[2]
        self.sensor1 = sensor[0]
        self.sensor2 = sensor[1]
        self.sensor3 = sensor[2]
        self.sensor4 = sensor[3]


    basic = Basic(self.ev3, [self.motorb, self.motorc, self.motord], [self.sensor1, self.sensor2, self.sensor3, self.sensor4])
    Movement(self.ev3, [self.motorb, self.motorc, self.motord], [self.sensor1, self.sensor2, self.sensor3, self.sensor4], basic)
    Tasks(self.ev3, [self.motorb, self.motorc, self.motord], [self.sensor1, self.sensor2, self.sensor3, self.sensor4], basic, human)
    