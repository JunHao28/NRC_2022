class Tasks:

    def __init__(self, ev3, motor, sensor, basic, human, movement, wait):
        self.ev3 = ev3
        self.motorb = motor[0]
        self.motorc = motor[1]
        self.motord = motor[2]
        self.sensor1 = sensor[0]
        self.sensor2 = sensor[1]
        self.sensor3 = sensor[2]
        self.sensor4 = sensor[3]
        self.basic = basic
        self.human = human
        self.movement = movement
        self.wait = wait

    def checkColour(self, rgbValue, direction, box, moveForward=False, special=False, corner=False):
        # Direction: Left 1, Right 2
        # Box: Red 1, Brown 2, Yellow 3, White 4, Green 5, Blue 6
        # Special (Got wall for collecting chemical)
        if rgbValue[2] > 10 and sum(rgbValue) > 130 and rgbValue[0] - rgbValue[1] < 5 and rgbValue[0] - rgbValue[1] > -5 and rgbValue[1] - rgbValue[2] < 5 and rgbValue[1] - rgbValue[2] > -5:
            self.collectChemical(direction, special, corner)
            return True
        elif rgbValue[0] >= 50 and rgbValue[1] <= 50 and rgbValue[2] <= 50:
            self.depositWater()
            return True
        elif sum(rgbValue) > 250:
            if self.human[0] == 0:
                self.human[0] = box
                return True
            else:
                self.human[1] = box
                return True
        else:
            return False

    def depositWater(self):
        self.motord.run_target(1500, 90)
        self.motord.run(500)
        self.wait(1)
        self.motord.run(-500)
        self.motord.run_target(-1500, 0)

    def collectChemical(self, direction, special, corner):
        self.ev3.speaker.beep(frequency=700)
        if special == False:
            if corner == False:
                self.movement.gyrodegree(40, 200)
                self.movement.turn(0, (-2*direction+3)*90, oneWheel=direction)
                self.movement.gyrodegree(-160, 100)
                self.motord.run_target(-1500, 200)
                self.basic.stop()
                self.wait(0.5)
                self.movement.gyrodegree(160, 200)
                self.movement.turn(0, (-2*direction+3)*-90, oneWheel=direction)
            elif corner == True:
                # Change
                self.movement.gyrodegree(40, 200)
                self.movement.turn(0, (-2*direction+3)*90, oneWheel=direction)
                self.movement.gyrodegree(-160, 100)
                self.motord.run_target(-1500, 200)
                self.basic.stop()
                self.wait(0.5)
                self.movement.gyrodegree(160, 200)
                self.movement.turn(0, (-2*direction+3)*-90, oneWheel=direction)
        elif special == True:
            # Change
            self.movement.gyrodegree(40, 200)
            self.movement.turn(0, (-2*direction+3)*90, oneWheel=direction)
            self.movement.gyrodegree(-160, 100)
            self.motord.run_target(-1500, 200)
            self.basic.stop()
            self.wait(0.5)
            self.movement.gyrodegree(160, 200)
            self.movement.turn(0, (-2*direction+3)*-90, oneWheel=direction)
    