import time
from pybricks.parameters import Port, Stop, Direction, Button, Color

class Robot:
    forwardki = 0
    forwardkp = 2
    forwardkd = 0
    gyroki = 0
    gyrokp = 3
    gyrokd = 0
    turnki = 0
    turnkp = 2.7
    turnkd = 0.2
    trackkp = 1 
    trackki = 0
    trackkd = 0


    startingPos = None
    
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
        self.motorb.brake()
        self.motorc.brake()

    def move(self, leftspeed, rightspeed):
        self.motorb.run(leftspeed)
        self.motorc.run(rightspeed)

    def resetRobot(self):
        self.motorb.reset_angle(0)
        self.motorc.reset_angle(0)
        self.motord.reset_angle(0)
        self.sensor1.reset_angle(0)

    def sensorVal(self, sensorNo):
        sensors = [self.sensor1, self.sensor2, self.sensor3, self.sensor4]
        if sensorNo == 0:
            return sensors[sensorNo].angle()
        else:
            return sensors[sensorNo].rgb()
    
    def pidturn(self, speed, degree, minimumSpeed=30, oneWheel=0):
        currentAngle = self.sensor1.angle()
        integral = 0
        lastError = 0
        while self.sensorVal(0) != (currentAngle + degree):
            error = self.sensor1.angle() - (currentAngle + degree)
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
        self.stop()

    def pidmovedistance(self, degree, speed, minimumSpeed=200, move=True, currentAngle=0, last_error=0, derivative=0):
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
    
    def pidmovegyrodegree(self, degree, speed, minimumSpeed=100):
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

    def gyroForwardTillSense(self, speed, sensorNo, rgb, minimumSpeed=200, stopAfter=None):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        gyroIntegral = 0
        gyroDerivative = 0
        gyroLastError = 0
        sensor = self.sensorVal(sensorNo)
        while ((sum(sensor) <= rgb+20) and (sum(sensor) >= rgb-20)) == False:
            gyroError = self.sensorVal(0) - currentDegree
            gyroIntegral = gyroIntegral + gyroError
            gyroDerivative = gyroError - gyroLastError
            gyroLastError = gyroError
            changeSpeed = CheckLimit.maximum((gyroDerivative * self.gyrokd) + (gyroError * self.gyrokp) + (gyroIntegral * self.gyroki), 200)
            self.move(CheckLimit.minimaximum(speed+changeSpeed, minimumSpeed, 1200), CheckLimit.minimaximum(speed-changeSpeed, minimumSpeed, 1200))
            if stopAfter != None:
                if currentAngle + stopAfter <= self.motorb.angle():
                    break
                    return None
            sensor = self.sensorVal(sensorNo)
        self.stop()
        return self.sensorVal(sensorNo+1)
    
    def pidLineTracking(self, rgb, speed, sensor, rgb2):
        integral = 0
        lastError = 0
        print(self.sensorVal(3))
        while sum(self.sensorVal(sensor)) < rgb2:
            error = sum(self.sensorVal(1)) - rgb
            integral = integral + error
            derivative = error - lastError
            lastError = error
            change = CheckLimit.maximum((derivative * self.trackkd) + (error * self.trackkp) + (integral * self.trackki), 200)
            print(change)
            self.move(-speed - change, -speed + change)
        self.stop()

    def depositWater(self):
        self.motord.run_target(1500, 90)
        self.motord.run(500)
        time.sleep(1)
        self.motord.run(-500)
        self.motord.run_target(-1500, -1)

            

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