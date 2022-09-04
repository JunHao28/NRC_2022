import time
from pybricks.parameters import Port, Stop, Direction, Button, Color
from functions.unchanged.PID import PID
from functions.unchanged.CheckLimit import CheckLimit



class Movement:

    #PID values
    gyros = PID(83, 0, 0)
    gyro2 = PID(10, 0, 5)
    oneWheelTurn = PID(0.95, 0.01, 0)
    twoWheelTurn = PID(0.16, 0.00898, 0)
    track = PID(1.3, 0, 5)
    track2 = PID(3, 0, 10)

    def __init__(self, ev3, motor, sensor, basic):
        self.ev3 = ev3
        self.motorb = motor[0]
        self.motorc = motor[1]
        self.motord = motor[2]
        self.sensor1 = sensor[0]
        self.sensor2 = sensor[1]
        self.sensor3 = sensor[2]
        self.sensor4 = sensor[3]
        self.basic = basic

    def turn(self, speed, degree, oneWheel=0):
        # C wheel turn: 1
        # B wheel turn: 2
        currentAngle = self.basic.sense(0)
        errors = []
        result = [0, 0, 0]
        if oneWheel == 0:
            minimumSpeed=30
            maximumSpeed=700
            decelDeg=64
        else:
            minimumSpeed=55
            maximumSpeed=1500
            decelDeg=70
        while True:
            error = self.basic.sense(0) - (currentAngle + degree)
            errors.append(error)
            if len(errors) >= 7:
                for i in range(7):
                    if errors[(len(errors) - i - 1)] != 0:
                        break
                    if i == 6:
                        return
            if error == 0:
                self.basic.stop()
            else:
                if error < 0 and result[1] > 0:
                    result[1] *= -1
                if error > 0 and result[1] < 0:
                    result[1] *= -1

                if abs(error) >= decelDeg:
                    speed = maximumSpeed
                else:
                    speed = minimumSpeed + (maximumSpeed - minimumSpeed) * ((abs(error) / decelDeg) ** 2)
                if error < 0:
                    speed *= -1
                right = -speed if (oneWheel != 1) else 0
                left = speed if (oneWheel != 2) else 0
                self.basic.move(left, right)

    def moveTillStall(self, speed):
        motorb = []
        motorc = []
        while True:
            motorb.append(self.motorb.angle())
            motorc.append(self.motorc.angle())
            if len(motorb) > 30 and len(motorc) > 30:
                motorb.pop(0)
                motorc.pop(0)
                if len(set(motorb)) == 1 and len(set(motorc)) == 1:
                    self.basic.stop()
                    return
            self.basic.move(speed, speed)

    def decelerate(self, degree, startingSpeed=10, accelDist=40, maximumSpeed=1300, minimumSpeed=200, move=True, currentAngle=0):
        if move:
            currentAngle = self.motorb.angle()
            result = [0, 0, 1000]
        finalAngle = abs(self.motorb.angle()-currentAngle)
        degree = abs(degree)
        decelDist = (maximumSpeed-minimumSpeed) * ((550/1100)**2)
        while finalAngle <= degree:
            if finalAngle <= accelDist:
                speed = startingSpeed + (maximumSpeed - startingSpeed) * ((finalAngle / accelDist) ** 2)
            elif (degree-finalAngle) <= decelDist:
                speed = minimumSpeed + (maximumSpeed - minimumSpeed) * (((degree - finalAngle) / decelDist) ** 2)
            elif (degree-finalAngle) <= 50:
                speed = minimumSpeed
            else: 
                speed = maximumSpeed
            if move:
                self.basic.move(speed, speed)
            else:
                return speed
            finalAngle = abs(self.motorb.angle()-currentAngle)
        self.basic.stop()
        return None

    def gyro(self, pid, speed=700, condition=None, minimumSpeed=0, override=None, inputs=None):
        outputs = [0, 0, 0]
        if inputs == None:
            currentDegree = self.sensor1.angle()
        else:
            outputs[1] = inputs[0]
            outputs[2] = inputs[1]
            currentDegree = inputs[2]
        if override != None:
            currentDegree = override
        while True:
            gyroError = self.sensor1.angle() - currentDegree
            outputs = pid.pid(gyroError, outputs[1], outputs[2])
            rightspeed = (speed - outputs[0]) if (speed > 0) else speed - outputs[0]
            leftspeed = speed + outputs[0] if(speed > 0) else speed + outputs[0]
            if condition != None and condition():
                return
            if inputs != None:
                return [outputs[1], outputs[2], CheckLimit.minimaximum(leftspeed, minimumSpeed, 1500), CheckLimit.minimaximum(rightspeed, minimumSpeed, 1500)]
            else:
                self.basic.move(CheckLimit.minimaximum(leftspeed, minimumSpeed, 1500),
                                CheckLimit.minimaximum(rightspeed, minimumSpeed, 1500))
        self.basic.stop()

    def gyrodegree(self, speed, degree, startingSpeed=0, accelDist=40, maximumSpeed=1300, minimumSpeed=200, stop=True, override=None, decel=True, times=True):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        if override != None:
            currentDegree = override
        output = [0, 0, 0, 0]
        while True:
            if decel == True:
                pidDistance = self.decelerate(degree, startingSpeed=startingSpeed, accelDist=accelDist, maximumSpeed=maximumSpeed, minimumSpeed=minimumSpeed, move=False, currentAngle=currentAngle)
            else:
                finalAngle = abs(self.motorb.angle()-currentAngle)
                degrees = abs(degree)
                if finalAngle < degrees:
                    pidDistance = abs(speed)
                else: 
                    pidDistance = None
            if pidDistance == None:
                break
            output = self.gyro(self.gyros, speed=abs(speed)* (3 if times else 1), minimumSpeed=0, inputs=[output[0], output[1], currentDegree], override=override)
            output[2] *= pidDistance/1300
            output[3] *= pidDistance/1300
            left = CheckLimit.minimaximum(output[2]+pidDistance, minimumSpeed, 1500)
            right = CheckLimit.minimaximum(output[3]+pidDistance, minimumSpeed, 1500)
            self.basic.move(left, right) if degree > 0 else self.basic.move(-right, -left)
        if stop:
            self.basic.stop()

    def gyroTillSense(self, speed, condition, minimumSpeed=20, stopAfter=None, override=None, stop=True):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        outputs = [0, 0]
        if override != None:
            currentDegree = override
        while True:
            # print(self.sensor1.angle())
            output = self.gyro(self.gyro2, speed=speed, minimumSpeed=minimumSpeed, inputs=[outputs[0], outputs[1], currentDegree], override=override)
            self.basic.move(output[2], output[3])
            if condition():
                if stop:
                    self.basic.stop() 
                return True
            elif (stopAfter != None and (abs(stopAfter) <= abs(self.motorb.angle()-currentAngle))):
                if stop:
                    self.basic.stop() 
                return 
        return

    def pidLineTracking(self, rgb, speed, returnVal=None, condition=lambda: True, pid=None):
        result = [0, 0, 0]
        if returnVal != None:
            result = returnVal
        while condition():
            error = self.sensor2.reflection() - rgb
            result = pid.pid(error, result[1], result[2], change=1)
            change = CheckLimit.maximum(result[0], 1500-speed)
            if returnVal == None:
                self.basic.move(-speed - change, - speed + change)
            else:
                return [-speed - change, - speed + change, result[1], result[2]]
        self.basic.stop()

    def lineTrackingTillSense(self, rgb, speed, condition, stopAfter=None, whiteblack=True, pid=None):
        if pid == None:
            pid = self.track
        returnVal = [0, 0, 0, 0]
        currentAngle = self.motorb.angle()
        while True:
            returnVal = self.pidLineTracking(rgb, speed, returnVal=[0, returnVal[2], returnVal[3]], pid=pid)
            self.basic.move(returnVal[0 if whiteblack else 1], returnVal[1 if whiteblack else 0])
            if condition() or (stopAfter != None and (abs(stopAfter) <= abs(self.motorb.angle()-currentAngle))):
                self.basic.stop()
                return
