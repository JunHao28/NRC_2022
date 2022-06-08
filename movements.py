import time
from pybricks.parameters import Port, Stop, Direction, Button, Color


# pidturn(self, speed, degree, minimumSpeed=10, oneWheel=0)
# pidmovedistance(self, degree, speed, minimumSpeed=200, move=True, currentAngle=0, last_error=0, derivative=0)
# pidmovegyrodegree(self, degree, speed, minimumSpeed=100)
# gyroForwardTillSense(self, speed, sensorNo, rgb, minimumSpeed=200, stopAfter=None, leeway1=10, leeway2=10)
# pidLineTracking(self, rgb, speed, sensor, rgb2)

class Robot:

    #PID values
    forwardki = 0.001
    forwardkp = 3
    forwardkd = 2
    gyroki = 0
    gyrokp = 5
    gyrokd = 0
    oneWheelTurnki = 0.00000002
    oneWheelTurnkp = 15
    oneWheelTurnkd = 8
    twoWheelTurnki = 0.00000002
    twoWheelTurnkp = 7.5
    twoWheelTurnkd = 4
    trackkp = 1.4
    trackki = 0
    trackkd = 3

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
    
    def pidturn(self, speed, degree, minimumSpeed=15, oneWheel=0):
        # Right wheel turn: 1
        # Left wheel turn: 2
        currentAngle = self.sensor1.angle()
        integral = 0
        lastError = 0
        errors = []
        while True:
            error = self.sensor1.angle() - (currentAngle + degree)
            errors.append(error)
            if len(errors) >= 7:
                for i in range(7):
                    if errors[(len(errors) - i - 1)] != 0:
                        break
                    if i == 6:
                        return
            if error == 0:
                self.stop()
            else: 
                integral = integral + error
                derivative = error - lastError
                lastError = error
                if oneWheel != 0:
                    changeSpeed = (derivative * self.oneWheelTurnkd) + (error * self.oneWheelTurnkp) + (integral * self.oneWheelTurnki)
                else:
                    changeSpeed = (derivative * self.twoWheelTurnkd) + (error * self.twoWheelTurnkp) + (integral * self.twoWheelTurnki)
                if changeSpeed > 0:
                    changeSpeed += speed
                else:
                    changeSpeed -= speed
                changeSpeed = CheckLimit.minimaximum(changeSpeed, minimumSpeed, 1500)
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

    def pidmovedistance(self, degree, speed, minimumSpeed=100, move=True, currentAngle=0, last_error=0, integral=0, derivative=0):
        if move:
            currentAngle = self.motorb.angle()
        while degree != self.motorb.angle() - currentAngle:
            error = degree - (self.motorb.angle()-currentAngle)
            derivative = error - last_error
            speed = (derivative * self.forwardkd) + (error * self.forwardkp) + (integral * self.forwardki)
            last_error = error
            speed = CheckLimit.minimaximum(speed, minimumSpeed, 1500)
            if move:
                self.move(speed, speed)
            else:
                return [speed, last_error, derivative, integral]
    
    def pidmovegyrodegree(self, degree, speed, minimumSpeed=50, override=None):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        if override != None:
            currentDegree=override
        rgbValue = self.sensorVal(2)
        if rgbValue[2] > 10 and sum(rgbValue) > 60 and rgbValue[0] - rgbValue[1] < 5 and rgbValue[0] - rgbValue[1] > -5 and rgbValue[1] - rgbValue[2] < 5 and rgbValue[1] - rgbValue[2] > -5:
            self.beep()
        gyroIntegral = 0
        gyroDerivative = 0
        gyroLastError = 0
        pidDistance = [0, 0, 0, 0]
        while degree != currentAngle:
            pidDistance = self.pidmovedistance(degree, speed, minimumSpeed=minimumSpeed, move=False, currentAngle=currentAngle, last_error=pidDistance[1], derivative=pidDistance[2], integral=pidDistance[3])
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

    def gyroForwardTillSense(self, speed, sensorNo, rgb, minimumSpeed=200, stopAfter=None, leeway1=10, leeway2=10, condition=None, override=None, backwards=False):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        gyroIntegral = 0
        gyroDerivative = 0
        gyroLastError = 0
        sensor = self.sensorVal(sensorNo)
        if override != None:
            currentDegree = override
        while True:
            gyroError = self.sensorVal(0) - currentDegree
            gyroIntegral = gyroIntegral + gyroError
            gyroDerivative = gyroError - gyroLastError
            gyroLastError = gyroError
            
            changeSpeed = CheckLimit.maximum((gyroDerivative * self.gyrokd) + (gyroError * self.gyrokp) + (gyroIntegral * self.gyroki), 200)
            if backwards == False:
                self.move(CheckLimit.minimaximum(speed+changeSpeed, minimumSpeed, 1200), CheckLimit.minimaximum(speed-changeSpeed, minimumSpeed, 1200))
            else: 
                self.move(CheckLimit.minimaximum(-speed-changeSpeed, minimumSpeed, 1200), CheckLimit.minimaximum(-speed+changeSpeed, minimumSpeed, 1200))
            sensor = self.sensorVal(sensorNo)
            if ((sum(sensor) <= rgb+leeway1) and (sum(sensor) >= rgb-leeway2)) != False:
                self.stop()
                return sensor
            elif condition != None and (condition()) == False:
                self.stop()
                return None
            elif stopAfter != None and stopAfter > 0 and (currentAngle + stopAfter <= self.motorb.angle()):
                self.stop()
                return None
            elif stopAfter != None and stopAfter < 0 and (currentAngle + stopAfter >= self.motorb.angle()):
                self.stop()
                return None
            sensor = self.sensorVal(sensorNo)
        self.stop()
        return self.sensorVal(sensorNo)
    
    def pidLineTracking(self, rgb, speed, returnVal=None):
        lastError = 0
        if returnVal != None:
            lastError = returnVal
        # while sum(self.sensorVal(sensor)) < rgb2:
        while True:
            error = self.sensor2.reflection() - rgb
            derivative = error - lastError
            lastError = error
            change = CheckLimit.maximum((derivative * self.trackkd) + (error * self.trackkp), 1500-speed)
            if returnVal==None:
                self.move(-speed + change, - speed - change)
            else: 
                return [-speed + change, - speed - change, lastError]
        self.stop()
    
    def lineTrackingTillSense(self, rgb, speed, condition1):
        lastError = 0
        while True: 
            returnVal = self.pidLineTracking(rgb, speed, returnVal=lastError)
            lastError = returnVal[2]
            self.move(returnVal[0], returnVal[1])
            if condition1():
                self.stop()
                return 

    def checkColour(self, rgbValue, direction, box, moveForward=False):
        #Direction: Left 1, Right 2
        #Box: Red 1, Brown 2, Yellow 3, White 4, Green 5, Blue 6
        print(rgbValue)
        if rgbValue[2] > 10 and sum(rgbValue) > 90 and rgbValue[0] - rgbValue[1] < 5 and rgbValue[0] - rgbValue[1] > -5 and rgbValue[1] - rgbValue[2] < 5 and rgbValue[1] - rgbValue[2] > -5:
            self.collectChemical(direction)
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
        time.sleep(1)
        self.motord.run(-500)
        self.motord.run_target(-1500, 0)

    def collectChemical(self, direction):
        self.pidmovegyrodegree(40, 200)
        self.pidturn(0, (-2*direction+3)*90, oneWheel=direction)
        self.pidmovegyrodegree(-160, 100)
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