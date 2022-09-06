class Tasks:

    def __init__(self, ev3, motor, sensor, colour, basic, human, chemical, fire, movement, wait, printtxt):
        self.ev3 = ev3
        self.motorb = motor[0]
        self.motorc = motor[1]
        self.motord = motor[2]
        self.sensor1 = sensor[0]
        self.sensor2 = sensor[1]
        self.sensor3 = sensor[2]
        self.sensor4 = sensor[3]
        self.colour = colour
        self.basic = basic
        self.human = human
        self.fire = fire
        self.chemical = chemical
        self.movement = movement
        self.wait = wait
        self.lastSense = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.lastSense2 = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.print = printtxt

    def reset(self):
        self.lastSense = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.lastSense2 = [[0, 0, 0, 0], [0, 0, 0, 0]]
    
    def returnchem(self):
        return self.chemical

    def change(self, rgb, rgb2, side):

        self.lastSense[side] = []
        for x in rgb:
            self.lastSense[side].append(x)
        self.lastSense2[side] = []
        for x in rgb2:
            self.lastSense2[side].append(x)

    def checkColour(self, side, box, moveForward=False, special=0):
        # Direction: Left 1, Right 2
        # Box: Red 1, Brown 2, Yellow 3, White 4, Green 5, Blue 6
        # Special (Got wall for collecting chemical)
        degree = self.basic.sense(0)
        if degree%90 > 45: 
            degree = degree + 90 - (degree%90)
        elif degree%90 != 0:
            degree = degree - (degree%90)
        rgbValue = self.basic.sense(side)
        rgbValue2 = self.basic.sense(side+2)
        rgbValue3 = self.basic.sense(side+7)
        if self.lastSense[side-2] == [0, 0, 0, 0] or self.lastSense2[side-2] == [0, 0, 0, 0]:
            self.lastSense[side-2] = rgbValue2
            self.lastSense2[side-2] = rgbValue3
            self.print("First detection:", self.lastSense, self.lastSense2)
            return False
        else:
            # print(self.lastSense)
            diff = abs(sum(self.lastSense[side-2]) - sum(rgbValue2))
            self.print("lastSense", self.lastSense, self.lastSense2)
            diff2 = abs(round(self.lastSense2[side-2][3], 1) - round(rgbValue3[3], 1))
            self.print("spikeVal", diff, diff2)
            for x in range(len(self.lastSense[side-2])):
                if (self.lastSense[side-2][0] - rgbValue2[0]) >= 20 or diff >= 35 or (diff2 >=3 and diff2 <= 4.5):
                    self.basic.stop()
                    self.change(rgbValue2, rgbValue3, side-2)
                    break
                if x == 3:
                    self.change(rgbValue2, rgbValue3, side-2)
                    return False
        if diff <= 40:
            self.movement.gyrodegree(200, -2, override=degree, decel=False)
            rgbValue3 = self.basic.sense(side)
            rgbValue4 = self.basic.sense(side+2)
            # print(rgbValue, rgbValue2, rgbValue3, rgbValue4)
            returnVal = self.movement.gyroTillSense(-300, lambda: ((sum(self.basic.sense(side+2)) - sum(rgbValue2)) > 10 or abs(self.basic.sense(side+2)[0] - rgbValue2[0]) > 10), stopAfter=-20)
            if returnVal != True:
                print("Chemical?:", rgbValue, rgbValue2, rgbValue3, rgbValue4)
                if self.colour["chemical"].condition(rgbValue, rgbValue2) or self.colour["chemical"].condition(rgbValue3, rgbValue4):
                    self.basic.stop()
                    self.collectChemical(2 if side==2 else 1, degree, special=special)
                    self.reset()
                    return True
            rgbValue = self.basic.sense(side)
            rgbValue2 = self.basic.sense(side+2) 
            self.basic.stop()
        if self.colour["fire"].condition(rgbValue):
            self.movement.gyrodegree(-100, -20, override=degree)
            self.basic.stop()
            self.depositWater()
            self.reset()
            return True
        elif self.colour["human"].condition(rgbValue, rgbValue2):
            self.ev3.speaker.beep(frequency=800)
            self.basic.beep()
            if self.human[0] == 0:
                self.human[0] = box
            else:
                self.human[1] = box            
            self.reset()
            return True
        else:
            return False

    def depositWater(self):
        if self.fire[0] == True:
            self.fire[1] = True
        else:
            self.fire[0] = True
        self.motord.run_until_stalled(-1500, )
        self.motord.stop()
        self.wait(0.3)
        self.motord.run_target(1500, 0 if self.chemical == False else -210)

    def collectYellow(self):
        self.motord.run_target(1500, -150)

    def depositYellow(self):
        self.motord.run_target(1500, 70)

    def collectChemical(self, direction, degree, special=0):
        startAngle=self.motorb.angle()
        self.chemical = True
        self.basic.stop()
        self.ev3.speaker.beep(frequency=700)
        
        if special == 0:
            self.movement.gyrodegree(150, 40, maximumSpeed=250, accelDist=1, override=degree)
            self.wait(0.2)
            self.movement.turn(0, (degree+(90 if direction == 2 else -90)) - self.basic.sense(0), oneWheel=direction)
            self.movement.gyrodegree(-60, -185, decel=False, override=degree+(90 if direction == 2 else -90))
            self.wait(0.2)
            self.motord.run_target(1500, -200)
            self.basic.stop()
            self.movement.gyrodegree(60, 185, decel=False, override=degree+(90 if direction == 2 else -90))
            self.motord.run_target(1500, -220)
            self.wait(0.2)
            self.movement.turn(0, degree - self.basic.sense(0), oneWheel=direction)
            self.movement.gyrodegree(150, -40, maximumSpeed=300, accelDist=1, override=degree)
        elif special == 1:
            self.movement.gyrodegree(1, 180, maximumSpeed=300, accelDist=1, override=degree)
            self.wait(0.2)
            self.movement.turn(0, (degree+(90 if direction == 2 else -90)) - self.basic.sense(0))
            self.wait(0.2)
            self.movement.gyrodegree(-60, -100, decel=False, override=degree+(90 if direction == 2 else -90))
            self.wait(0.2)
            self.motord.run_target(1500, -250)
            self.basic.stop()
            self.movement.gyrodegree(60, 100, decel=False, override=degree+(90 if direction == 2 else -90))
            self.wait(0.2)
            self.movement.turn(0, degree - self.basic.sense(0),)
            self.wait(0.2)
            self.movement.gyrodegree(1, -180, maximumSpeed=300, accelDist=1, override=degree)
        elif special == 2:
            if direction == 2:
                self.movement.turn(0, 90, oneWheel=1)
                self.movement.turn(0, 55, oneWheel=2)
                self.movement.gyrodegree(-1, -175, maximumSpeed=201, accelDist=1)
                self.motord.run_target(1500, -200)
                self.movement.gyrodegree(1, 175, maximumSpeed=201, accelDist=1)
                self.movement.turn(0, -55, oneWheel=2)
                self.movement.turn(0, degree-self.basic.sense(0), oneWheel=1)
                self.basic.stop()
            else:
                self.movement.turn(0, -90, oneWheel=2)
                self.movement.turn(0, -55, oneWheel=1)
                self.movement.gyrodegree(-1, -175, maximumSpeed=201, accelDist=1)
                self.motord.run_target(1500, -200)
                self.movement.gyrodegree(1, 175, maximumSpeed=201, accelDist=1)
                self.movement.turn(0, 55, oneWheel=1)
                self.movement.turn(0, degree-self.basic.sense(0), oneWheel=2)
                self.basic.stop()

            # self.wait(0.2)
            # self.movement.gyrodegree(200, -70, decel=False, override=degree)
            # self.wait(0.2)
            # self.movement.turn(0, (135 if direction == 2 else -135))
            # self.wait(0.2)
            # self.movement.gyrodegree(-40, -160, decel=False)
            # self.wait(0.2)
            # self.motord.run_target(1500, -210)
            # self.basic.stop()
            # self.movement.gyrodegree(40, 160, decel=False)
            # self.motord.run_target(1500, 0)
            # self.wait(0.2)
            # self.movement.gyrodegree(-40, -100, decel=False)
            # self.wait(0.2)
            # self.motord.run_target(1500, -210)
            # self.basic.stop()
            # self.movement.gyrodegree(40, 100, decel=False)
            # self.wait(0.2)
            # self.movement.turn(0, degree - self.basic.sense(0))
            # self.wait(0.2)

        self.motorb.reset_angle(startAngle)
