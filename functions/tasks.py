class Tasks:

    def __init__(self, ev3, motor, sensor, colour, basic, human, chemical, fire, movement, wait):
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

    def reset(self):
        lastSense = [[0, 0, 0, 0], [0, 0, 0, 0]]

    def change(self, rgb, side):

        self.lastSense[side] = []
        for x in rgb:
            self.lastSense[side].append(x)

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
        if self.lastSense[side-2] == [0, 0, 0, 0]:
            self.lastSense[side-2] = rgbValue2
            return False
        else:
            for x in range(len(self.lastSense[side-2])):
                if (self.lastSense[side-2][x] - rgbValue2[x]) >= 15 or abs(sum(self.lastSense[side-2]) - sum(rgbValue2)) >= 10:
                    self.basic.stop()
                    self.change(rgbValue2, side-2)
                    break
                if x == 3:
                    self.change(rgbValue2, side-2)
                    return False
        self.movement.gyrodegree(50, -2, override=degree)
        rgbValue3 = self.basic.sense(side)
        rgbValue4 = self.basic.sense(side+2)
        returnVal = self.movement.gyroTillSense(-100, lambda:   ((sum(self.basic.sense(side+2)) - sum(rgbValue2)) > 30 or abs(self.basic.sense(side+2)[0] - rgbValue2[0]) > 20), stopAfter=-15)
        if returnVal != True:
            if self.colour["chemical"].condition(rgbValue, rgbValue2) or self.colour["chemical"].condition(rgbValue3, rgbValue4):
                self.basic.stop()
                self.collectChemical(2 if side==2 else 1, degree, special=special)
                self.lastSense[side-2] = [0, 0, 0, 0]
                return True
        rgbValue = self.basic.sense(side)
        rgbValue2 = self.basic.sense(side+2) 
        self.basic.stop()
        if self.colour["fire"].condition(rgbValue):
            self.basic.stop()
            self.depositWater()
            self.movement.gyrodegree(-100, -20, override=degree)
            self.lastSense[side-2] = [0, 0, 0, 0]
            return True
        elif self.colour["human"].condition(rgbValue, rgbValue2):
            self.ev3.speaker.beep(frequency=800)
            self.basic.beep()
            if self.human[0] == 0:
                self.human[0] = box
            else:
                self.human[1] = box            
            self.lastSense[side-2] = [0, 0, 0, 0]
            return True
        else:
            return False

    def depositWater(self):
        self.motord.run_until_stalled(-1500, )
        self.motord.stop()
        self.motord.run_target(1500, 0 if self.chemical == False else -250)

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
            self.movement.gyrodegree(150, 35, maximumSpeed=250, accelDist=1, override=degree)
            self.wait(0.2)
            self.movement.turn(0, (90 if direction == 2 else -90) - self.basic.sense(0), oneWheel=direction)
            self.movement.gyrodegree(-60, -180, decel=False, override=degree+(90 if direction == 2 else -90))
            self.wait(0.2)
            self.motord.run_target(1500, -250)
            self.basic.stop()
            self.movement.gyrodegree(60, 180, decel=False, override=degree+(90 if direction == 2 else -90))
            self.wait(0.2)
            self.movement.turn(0, (-90 if direction == 2 else 90) - self.basic.sense(0), oneWheel=direction)
            self.movement.gyrodegree(150, -35, maximumSpeed=300, accelDist=1, override=degree)
        elif special == 1:
            self.movement.gyrodegree(150, 100, maximumSpeed=300, accelDist=1, override=degree)
            self.wait(0.2)
            self.movement.turn(0, (90 if direction == 2 else -90) - self.basic.sense(0))
            self.wait(0.2)
            self.movement.gyrodegree(-60, -100, decel=False, override=degree+(90 if direction == 2 else -90))
            self.wait(0.2)
            self.motord.run_target(1500, -250)
            self.basic.stop()
            self.movement.gyrodegree(60, 100, decel=False, override=degree+(90 if direction == 2 else -90))
            self.wait(0.2)
            self.movement.turn(0, (-90 if direction == 2 else 90) - self.basic.sense(0),)
            self.wait(0.2)
            self.movement.gyrodegree(150, -100, maximumSpeed=300, accelDist=1, override=degree)
        elif special == 2:
            self.wait(0.2)
            self.movement.gyrodegree(200, -20, decel=False, override=degree)
            self.wait(0.2)
            self.movement.turn(0, (135 if direction == 2 else -135) - self.basic.sense(0))
            self.wait(0.2)
            self.movement.gyrodegree(-40, -130, decel=False)
            self.wait(0.2)
            self.motord.run_target(1500, -250)
            self.basic.stop()
            self.movement.gyrodegree(40, 130, decel=False, override=degree)
            self.wait(0.2)
            self.movement.turn(0, (-135 if direction == 2 else 135) - self.basic.sense(0))
            self.wait(0.2)

        self.motorb.reset_angle(startAngle)
