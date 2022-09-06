from functions.movements import Movement
from functions.basic import Basic
from functions.tasks import Tasks
from pybricks.parameters import Port, Stop, Direction, Button, Color


class Robot:

    printed=False

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
            
            "chemical": Colour("chemical", lambda val, val2: self.betw(sum(val2), 80, 140) and self.betw(val[0], 14, 22) and self.betw(val[1], 14, 22) and self.betw(val[2], 14, 22) and self.betw(val[3], 43, 49)),
            "fire": Colour("fire", lambda val: self.betw(val[0], 32, 47) and self.betw(val[1], 10, 15) and self.betw(val[2], 0, 14) and self.betw(val[3], 41, 48)),
            "human": Colour("human", lambda val, val2: sum(val2) > 200 and self.betw(val[0], 14, 30) and self.betw(val[1], 14, 30) and self.betw(val[2], 14, 30) and self.betw(val[3], 25, 48)),
            "line_tracking": 40,
            "line_tracking_2": 40,
            "line_tracking_3": 14,
        }
        self.startingPos = None
        self.human = [0, 0]
        self.chemical = False
        self.fire = [False, False]
        self.movement = Movement(ev3, motor, sensor, self.basic, self.print)
        self.tasks = Tasks(ev3, motor, sensor, self.colour, self.basic, self.human, self.chemical, self.fire, self.movement, lambda time: self.pause(time), self.print)

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
        sensorNo=[1, 6, 2, 4, 7, 9, 3, 5, 8, 10]
        sensorName=["ev3 rgb", "ev3 reflected", "3 percentage", "3 raw", "3 Norm", "3 Norm per", "4 parcentage", "4 raw", "4 Norm", "4 Norm per"]
        print(len(sensorNo))
        while True:
            if Button.UP in self.ev3.buttons.pressed():
                number+=1
                if number == len(sensorNo):
                    number = 0
            elif Button.DOWN in self.ev3.buttons.pressed():
                number-=1
                if number == -1:
                    number = len(sensorNo)-1
            print(number)
            self.ev3.screen.clear()
            self.ev3.screen.print(sensorName[number])
            values = self.basic.sense(sensorNo[number])
            if sensorNo[number] == 2 or sensorNo[number] == 3:
                for x in range(len(values)):
                    values[x] = int(values[x])
            self.ev3.screen.print(values)
            self.pause(0.2)
    
    def print(self, value):
        if not self.printed:
            with open('print.txt', 'w') as f:
                f.write(value)
            print("yes")
        else:
            with open('print.txt', 'a') as f:
                f.write(value)
            print("no")
        self.printed = True


class Colour:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def condition(self):
        return self.condition()