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

    def checkColour(self, rgbValue, direction, box, moveForward=False, special=0):
        # Direction: Left 1, Right 2
        # Box: Red 1, Brown 2, Yellow 3, White 4, Green 5, Blue 6
        # Special (Got wall for collecting chemical)
        # print(rgbValue)
        if self.colour["chemical"].condition(rgbValue):
            # self.collectChemical(direction, special=special)
            return True
        elif self.colour["fire"].condition(rgbValue):
            self.depositWater()
            return True
        elif self.colour["human"].condition(rgbValue):
            if self.human[0] == 0:
                self.human[0] = box
                return True
            else:
                self.human[1] = box
                return True
        else:
            return False

    def depositWater(self):
        self.motord.run_target(-1500, -90)
        self.motord.run(-500)
        self.wait(1)
        self.motord.run(500)
        self.motord.run_target(1500, 0 if self.chemical == False else 200)

    def collectChemical(self, direction, special=0):
        self.ev3.speaker.beep(frequency=700)
        if special == 0:
            self.movement.gyrodegree(200, 25)
            self.movement.turn(0, 90 if direction == 2 else -90, oneWheel=direction)
            self.movement.gyrodegree(-140, -130)
            self.wait(0.5)
            self.motord.run_target(1500, -150)
            self.basic.stop()
            self.wait(0.5)
            self.movement.gyrodegree(140, 100)
            self.movement.turn(0, -90 if direction == 2 else 90, oneWheel=direction)
            self.movement.gyrodegree(200, 25)
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

