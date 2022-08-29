class Tasks:

    def __init__(self, ev3, motor, sensor, colour, basic, human, chemical, movement, wait):
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
        self.chemical = chemical
        self.movement = movement
        self.wait = wait
        self.lastSense = [0, 0, 0, 0]

    def checkColour(self, side, box, moveForward=False, special=0):
        # Direction: Left 1, Right 2
        # Box: Red 1, Brown 2, Yellow 3, White 4, Green 5, Blue 6
        # Special (Got wall for collecting chemical)
        rgbValue = self.basic.sense(side)
        rgbValue2 = self.basic.sense(side+2)
        if self.lastSense == [0, 0, 0, 0]:
            self.lastSense = rgbValue2
            return False
        else:
            for x in range(len(self.lastSense)):
                if (self.lastSense[x] - rgbValue2[x]) >= 15 or abs(sum(self.lastSense) - sum(rgbValue2)) >= 13:
                    self.basic.stop()
                    self.lastSense = rgbValue2
                    break
                if x == 3:
                    self.lastSense = rgbValue2
                    return False 
        
        self.movement.gyroTillSense(100, lambda: abs(sum(self.basic.sense(side+2)) - sum(rgbValue2)) > 10, stopAfter=10)
            
        if self.colour["chemical"].condition(rgbValue, rgbValue2):
            self.basic.stop()
            self.collectChemical(2 if side=2 else 1, special=special)
            self.lastSense = [0, 0, 0, 0]
            return True
        elif self.colour["fire"].condition(rgbValue):
            self.basic.stop()
            self.depositWater()
            self.movement.gyrodegree(-100, -20)
            self.lastSense = [0, 0, 0, 0]
            return True
        elif self.colour["human"].condition(rgbValue, rgbValue2):
            self.ev3.speaker.beep(frequency=800)
            self.basic.beep()
            if self.human[0] == 0:
                self.human[0] = box
            else:
                self.human[1] = box            
            self.lastSense = [0, 0, 0, 0]
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

    def collectChemical(self, direction, special=0):
        startAngle=self.motorb.angle()
        self.chemical = True
        self.basic.stop()
        self.ev3.speaker.beep(frequency=700)
        if special == 0:
            self.movement.gyrodegree(200, 30)
            self.wait(0.2)
            self.movement.turn(0, 90 if direction == 2 else -90, oneWheel=direction)
            self.movement.gyrodegree(-60, -180, decel=False)
            self.wait(0.2)
            self.motord.run_target(1500, -250)
            self.basic.stop()
            self.wait(0.3)
            self.movement.gyrodegree(100, 180, decel=False)
            self.wait(0.2)
            self.movement.turn(0, -90 if direction == 2 else 90, oneWheel=direction)
            self.movement.gyrodegree(200, -70)
        elif special == 1:
            self.wait(0.3)
            self.movement.gyrodegree(200, 75)
            self.wait(0.3)
            self.movement.turn(0, 90 if direction == 2 else -90)
            self.wait(0.3)
            self.movement.gyrodegree(-40, -60, decel=False)
            self.wait(0.3)
            self.motord.run_target(1500, -250)
            self.basic.stop()
            # self.wait(0.3)
            self.movement.gyrodegree(40, 60, decel=False)
            self.wait(0.3)
            self.movement.turn(0, -90 if direction == 2 else 90,)
            self.wait(0.3)
            self.movement.gyrodegree(200, -75)
        elif special == 2:
            self.wait(0.3)
            self.movement.gyrodegree(200, -20)
            self.wait(0.3)
            self.movement.turn(0, 135 if direction == 2 else -135)
            self.wait(0.3)
            self.movement.gyrodegree(-40, -130, decel=False)
            self.wait(0.3)
            self.motord.run_target(1500, -250)
            self.basic.stop()
            # self.wait(0.3)
            self.movement.gyrodegree(40, 130, decel=False)
            self.wait(0.3)
            self.movement.turn(0, -135 if direction == 2 else 135)
            self.wait(0.3)

        self.motorb.reset_angle(startAngle)
