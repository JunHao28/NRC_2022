from functions.movements import Movement
from functions.basic import Basic
from functions.tasks import Tasks
from pybricks.parameters import Port, Stop, Direction, Button, Color


class Robot:

    startingPos = None
    human = [0, 0]
    chemical = True
    fire = [True, True]

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
            "red_floor": Colour("red_floor", lambda: (basic.sense(1)[0] > 60 or basic.sense(1)[1] < 10 or basic.sense(1)[2] < 10)),
            "brown_floor": Colour("brown_floor", lambda: (basic.sense(1)[0] > 15 and basic.sense(1)[0] < 40 and basic.sense(1)[1] < 15 and basic.sense(1)[2] < 15)), #Not done yet
            "yellow_floor": Colour("yellow_floor", lambda: (basic.sense(1)[0] > 60 and basic.sense(1)[1] > 40 and basic.sense(1)[2] < 30)),
            "blue_floor": Colour("blue_floor", lambda: (basic.sense(1)[0] < 15 and basic.sense(1)[1] < 30 and basic.sense(1)[2] > 40)),
            "green_floor": Colour("green_floor", lambda: (basic.sense(1)[0] < 15 and basic.sense(1)[1] > 30 and basic.sense(1)[2] < 20)),
            "white_floor": Colour("white_floor", lambda: (sensor[1].reflection() >= 72 and sum(basic.sense(1)) > 250)),
            
            "chemical": Colour("chemical", lambda val, val2: sum(val2) > 95 and sum(val2) < 140 and self.betw(val[0], 15, 20) and self.betw(val[1], 15, 20) and self.betw(val[2], 15, 20) and self.betw(val[3], 45, 49)),
            "fire": Colour("fire", lambda val: self.betw(val[0], 32, 47) and self.betw(val[1], 10, 15) and self.betw(val[2], 0, 14) and self.betw(val[3], 41, 48)),
            "human": Colour("human", lambda val, val2: sum(val2) > 250 and self.betw(val[0], 15, 28) and self.betw(val[1], 15, 28) and self.betw(val[2], 14, 28) and self.betw(val[3], 25, 45)),
            "line_tracking": 20,
            "line_tracking_2": 40,
            "line_tracking_3": 14,
        }
        self.movement = Movement(ev3, motor, sensor, self.basic)
        self.tasks = Tasks(ev3, motor, sensor, self.colour, self.basic, self.human, self.chemical, self.fire, self.movement, lambda time: self.pause(time))

    def pause(self, seconds):
        self.stop(seconds*1000)

    def neg(self, number):
        return int(self.startingPos) * number

    def side(self, right, left):
        if int(self.startingPos) == 1:
            return right
        elif int(self.startingPos) == -1:
            return left

    def betw(self, value, small, large):
        if value >= small and value <= large:
            return True
        else: 
            return False

    def start(self):
        self.ev3.light.on(Color.RED)
        buttons = self.ev3.buttons.pressed()
        while (not Button.CENTER in buttons):
            buttons = self.ev3.buttons.pressed()

    def callibrate(self):
        number=0
        sensorNo=[1, 6, 2, 4, 3, 5]
        sensorName=["ev3 rgb", "ev3 reflected", "3 percentage", "3 raw", "4 parcentage", "4 raw"]
        while True:
            if Button.UP in self.ev3.buttons.pressed():
                number+=1
                if number == len(sensorNo):
                    number = 0
            elif Button.DOWN in self.ev3.buttons.pressed():
                number-=1
                if number -1:
                    number = len(sensorNo)-1
            self.ev3.screen.clear()
            self.ev3.screen.print(sensorName[number])
            values = self.basic.sense(sensorNo[number])
            if number == 2 or number == 4:
                for x in range(len(values)):
                    values[x] = int(values[x]*100)
            self.ev3.screen.print(values)
            self.pause(0.2)
    

class Colour:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def condition(self):
        return self.condition()