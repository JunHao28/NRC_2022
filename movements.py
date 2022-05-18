import time
from pybricks.parameters import Port, Stop, Direction, Button, Color


# pidturn(self, speed, degree, minimumSpeed=10, oneWheel=0)
# pidmovedistance(self, degree, speed, minimumSpeed=200, move=True, currentAngle=0, last_error=0, derivative=0)
# pidmovegyrodegree(self, degree, speed, minimumSpeed=100)
# gyroForwardTillSense(self, speed, sensorNo, rgb, minimumSpeed=200, stopAfter=None, leeway1=10, leeway2=10)
# pidLineTracking(self, rgb, speed, sensor, rgb2)

class Robot:

    #PID values
    forwardki = 0
    forwardkp = 2
    forwardkd = 0
    gyroki = 0
    gyrokp = 4
    gyrokd = 0
    turnki = 0
    turnkp = 9
    turnkd = 0
    trackkp = 1 
    trackki = 0
    trackkd = 0

    #
    startingPos = None
    human = [0,0]


    def __init__(self, ev3, motorb, motorc, motord, sensor1, sensor2, sensor3, sensor4):
        self.ev3 = ev3
        self.motorb = motorb
        self.motorc = motorc
        self.motord = motord
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.sensor3 = sensor3
        self.sensor4 = sensor4

    def beep(self): 
        self.ev3.speaker.beep()

    def stop(self):
        self.motorb.hold()
        self.motorc.hold()
        self.motord.hold()

    def move(self, leftspeed, rightspeed):
        self.motorb.run(leftspeed)
        self.motorc.run(rightspeed)

    def resetRobot(self):
        self.motorb.reset_angle(0)
        self.motorc.reset_angle(0)
        self.motord.reset_angle(0)
        self.sensor1.reset_angle(0)
        self.motorb.control.limits(1500)
        self.motorc.control.limits(1500)

    def sensorVal(self, sensorNo):
        sensors = [self.sensor1, self.sensor2, self.sensor3, self.sensor4]
        if sensorNo == 0:
            return sensors[sensorNo].angle()
        else:
            return sensors[sensorNo].rgb()
    
    def pidturn(self, speed, degree, minimumSpeed=10, oneWheel=0):
        # Right wheel turn: 1
        # Left wheel turn: 2
        currentAngle = self.sensor1.angle()
        integral = 0
        lastError = 0
        errors = []
        while True:
            error = self.sensor1.angle() - (currentAngle + degree)
            errors.append(error)
            for i in range(10):
                if i == 9:
                    print(self.sensor1.angle())
                    return
                if errors[(len(errors) - i - 1)] != 0:
                    break
            if error == 0:
                self.stop()
            else: 
                integral = integral + error
                derivative = error - lastError
                lastError = error
                changeSpeed = (derivative * self.turnkd) + (error * self.turnkp) + (integral * self.turnki)
                if changeSpeed > 0:
                    changeSpeed += speed
                else:
                    changeSpeed -= speed
                changeSpeed = CheckLimit.minimaximum(changeSpeed, minimumSpeed, 1200)
                if (oneWheel == 0):
                    right = -changeSpeed
                    left = changeSpeed
                elif (oneWheel == 1):
                    right = -changeSpeed
                    left = 0
                elif (oneWheel == 2):
                    right = 0
                    left = changeSpeed
                self.move(left, right)

    def pidmovedistance(self, degree, speed, minimumSpeed=100, move=True, currentAngle=0, last_error=0, derivative=0):
        if move:
            currentAngle = self.motorb.angle()
        while degree != self.motorb.angle() - currentAngle:
            error = degree - (self.motorb.angle()-currentAngle)
            derivative = error - last_error
            speed = (derivative * self.forwardkd) + (error * self.forwardkp)
            last_error = error
            speed = CheckLimit.minimaximum(speed, minimumSpeed, 1500)
            if move:
                self.move(speed, speed)
            else:
                return [speed, last_error, derivative]
    
    def pidmovegyrodegree(self, degree, speed, minimumSpeed=80):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        gyroIntegral = 0
        gyroDerivative = 0
        gyroLastError = 0
        pidDistance = [0, 0, 0]
        while degree != currentAngle:
            pidDistance = self.pidmovedistance(degree, speed, minimumSpeed=minimumSpeed, move=False, currentAngle=currentAngle, last_error=pidDistance[1], derivative=pidDistance[2])
            if pidDistance == None:
                break
            gyroError = self.sensor1.angle() - currentDegree
            gyroIntegral = gyroIntegral + gyroError
            gyroDerivative = gyroError - gyroLastError
            gyroLastError = gyroError
            changeSpeed = CheckLimit.maximum((gyroDerivative * self.gyrokd) + (gyroError * self.gyrokp) + (gyroIntegral * self.gyroki), 200)
            leftspeed = pidDistance[0] + changeSpeed
            rightspeed = pidDistance[0] - changeSpeed
            self.move(CheckLimit.minimaximum(leftspeed, minimumSpeed, 1200), CheckLimit.minimaximum(rightspeed, minimumSpeed, 1200))
        self.stop() 

    def gyroForwardTillSense(self, speed, sensorNo, rgb, minimumSpeed=200, stopAfter=None, leeway1=10, leeway2=10, condition=None, override=None):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        gyroIntegral = 0
        gyroDerivative = 0
        gyroLastError = 0
        sensor = self.sensorVal(sensorNo)
        if override != None:
            print(True)
            currentDegree = override
        while True:
            gyroError = self.sensorVal(0) - currentDegree
            gyroIntegral = gyroIntegral + gyroError
            gyroDerivative = gyroError - gyroLastError
            gyroLastError = gyroError
            changeSpeed = CheckLimit.maximum((gyroDerivative * self.gyrokd) + (gyroError * self.gyrokp) + (gyroIntegral * self.gyroki), 200)
            self.move(CheckLimit.minimaximum(speed+changeSpeed, minimumSpeed, 1200), CheckLimit.minimaximum(speed-changeSpeed, minimumSpeed, 1200))
            # if condition != None:
            #     print(condition())
            #     print(sensor)
            if ((sum(sensor) <= rgb+leeway1) and (sum(sensor) >= rgb-leeway2)) != False:
                print(1)
                self.stop()
                return sensor
            elif condition != None and (condition()) == False:
                print(2)
                self.stop()
                return None
            elif stopAfter != None and (currentAngle + stopAfter <= self.motorb.angle()):
                print(3)
                self.stop()
                return None
            sensor = self.sensorVal(sensorNo)
        self.stop()
        return self.sensorVal(sensorNo)
    
    def pidLineTracking(self, rgb, speed, sensor, rgb2):
        integral = 0
        lastError = 0
        while sum(self.sensorVal(sensor)) < rgb2:
            error = sum(self.sensorVal(1)) - rgb
            integral = integral + error
            derivative = error - lastError
            lastError = error
            change = CheckLimit.maximum((derivative * self.trackkd) + (error * self.trackkp) + (integral * self.trackki), 200)
            self.move(-speed - change, -speed + change)
        self.stop()

    def checkColour(self, rgbValue, direction, box, moveForward=False):
        #Direction: Left 1, Right 2
        #Box: Red 1, Brown 2, Yellow 3, White 4, Green 5, Blue 6
        print(rgbValue)
        if sum(rgbValue) > 30 and rgbValue[0] - rgbValue[1] < 10 and rgbValue[0] - rgbValue[1] > -10 and rgbValue[1] - rgbValue[2] < 10 and rgbValue[1] - rgbValue[2] > -10:
            self.collectChemical(direction)
        elif rgbValue[0] > 60 and rgbValue[1] < 60 and rgbValue[2] < 60:
            self.depositWater()
        elif sum(rgbValue) > 250:
            if self.human[0] == 0:
                self.human[0] = box
            else: 
                self.human[1] = box

    def depositWater(self):
        self.motord.run_target(1500, 90)
        self.motord.run(500)
        time.sleep(1)
        self.motord.run(-500)
        self.motord.run_target(-1500, -1)

    def collectChemical(self, direction):
        self.pidmovegyrodegree(40, 200)
        self.pidturn(0, (-2*direction+3)*90, oneWheel=direction)
        self.pidmovegyrodegree(-160, 200)
        self.motord.run_target(-1500, 200)
        self.stop()
        time.sleep(0.5)
        self.pidmovegyrodegree(160, 200)
        self.pidturn(0, (-2*direction+3)*-90, oneWheel=direction)

            

class CheckLimit:
    def maximum(number: int, maximum: int):
        if number <= maximum:
            return number
        else:
            return maximum
    
    def minimum(number: int, minimum: int):
        if number >= minimum:
            return number
        else: 
            return minimum

    def minimaximum(number: int , minimum: int, maximum: int):
        if number < 0:
            minimum1 = minimum
            maximum1 = maximum
            minimum = -maximum1
            maximum = -minimum1
        return int(CheckLimit.minimum(CheckLimit.maximum(number, maximum), minimum))



class BaseSpeed:
    def __init__(self, leftBase, rightBase):
        self.leftBase = leftBase,
        self.rightBase = rightBase,

class StartingPos():
    RIGHT = 1
    LEFT = -1

    def __int__(self):
		return int('{0}'.format(self.value))