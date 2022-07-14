import time
from pybricks.parameters import Port, Stop, Direction, Button, Color
from functions.unchanged.PID import PID
from functions.unchanged.CheckLimit import CheckLimit


#robot.beep() (beep)
# robot.turn(speed, degree, oneWheel=0) (turning, oneWheel: (0, two wheel) (1, rightwheel) (2, leftwheel))

class Movement:

    # PID values
    forward = PID(6, 0, 3)
    gyros = PID(10, 0, 2.5)
    oneWheelTurn = PID(15, 0.000000025, 8)
    twoWheelTurn = PID(7.5, 0.000000025, 4)
    track = PID(1.4, 0, 3)

    # forwardki = 0.0001
    # forwardkp = 5
    # forwardkd = 2
    # gyroki = 0
    # gyrokp = 5
    # gyrokd = 0

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

    def turn(self, speed, degree, minimumSpeed=15, oneWheel=0):
        # Right wheel turn: 1
        # Left wheel turn: 2
        currentAngle = self.basic.sense(0)
        errors = []
        result = [0, 0, 0]
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
                result = self.oneWheelTurn.pid(error, result[1], result[2]) if (
                    oneWheel != 0) else self.twoWheelTurn.pid(error, result[1], result[2])
                if result[0] > 0:
                    result[0] += speed
                else:
                    result[0] -= speed
                result[0] = CheckLimit.minimaximum(
                    result[0], minimumSpeed, 1500)
                right = -result[0] if (oneWheel != 2) else 0
                left = result[0] if (oneWheel != 1) else 0
                self.basic.move(left, right)

    def decelerate(self, speed, degree, minimumSpeed=100, move=True, currentAngle=0, result=[0, 0, 0]):
        if move:
            currentAngle = self.motorb.angle()
            result = [0, 0, 1000]
        while degree != (self.motorb.angle() - currentAngle):
            error = degree - (self.motorb.angle()-currentAngle)
            result = self.forward.pid(error, result[1], result[2])
            result[0] = CheckLimit.minimaximum(result[0], minimumSpeed, 1500)
            if move:
                self.basic.move(result[0], result[0])
            else:
                return result

    def gyro(self, speed=700, condition=None, minimumSpeed=50, override=None, inputs=None):
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
            outputs = self.gyros.pid(gyroError, outputs[1], outputs[2])
            rightspeed = (speed - outputs[0]) if (speed >
                                                 0) else -(speed - outputs[0])
            leftspeed = speed + \
                outputs[0] if(speed > 0) else -(speed + outputs[0])
            if condition != None and condition():
                return
            if inputs != None:
                return [outputs[1], outputs[2], leftspeed, rightspeed]
            else:
                self.basic.move(CheckLimit.minimaximum(leftspeed, minimumSpeed, 1500),
                                CheckLimit.minimaximum(rightspeed, minimumSpeed, 1500))
        self.basic.stop()

    def gyrodegree(self, speed, degree, minimumSpeed=0, override=None):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        if override != None:
            currentDegree = override
        output = [0, 1000, 0, 0]
        pidDistance = [0, 0, 0]
        while True:
            pidDistance = self.decelerate(
                speed, degree, minimumSpeed=minimumSpeed, move=False, currentAngle=currentAngle, result=pidDistance)
            if pidDistance == None:
                break
            output = self.gyro(speed=700, minimumSpeed=minimumSpeed, inputs=[
                               output[0], output[1], currentDegree], override=override)
            self.basic.move(CheckLimit.minimaximum(output[2]+pidDistance[0], minimumSpeed, 1500),
                      CheckLimit.minimaximum(output[3]+pidDistance[0], minimumSpeed, 1500))
        self.basic.stop()

    def gyroTillSense(self, speed, condition, stopAfter=None, override=None):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        sensor = self.basic.sense(sensorNo)
        outputs = [0, 0]
        if override != None:
            currentDegree = override
        while True:
            output = self.gyro(speed, minimumSpeed=minimumSpeed, inputs=[
                outputs[0], outputs[1], currentDegree], override=override)
            self.basic.move(CheckLimit.minimaximum(
                output[2], minimumSpeed, 1500), CheckLimit.minimaximum(output[3], minimumSpeed, 1500))
            if (condition() == True) or (stopAfter != None and (abs(stopAfter) <= abs(self.motorb.angle()-currentAngle))):
                self.basic.stop()
                return None
        return

    def pidLineTracking(self, rgb, speed, returnVal=None):
        result = [0, 0, 0]
        if returnVal != None:
            result[1] = returnVal[2]
            result[2] = returnVal[3]
        while True:
            result = self.track.pid(error, result[1], result[2])
            change = CheckLimit.maximum(result[0], 1500-speed)
            if returnVal == None:
                self.basic.move(-speed + change, - speed - change)
            else:
                return [-speed + change, - speed - change, integral, lastError]
        self.basic.stop()

    def lineTrackingTillSense(self, rgb, speed, condition1):
        returnVal = [0, 0, 0, 0]
        while True:
            returnVal = self.pidLineTracking(speed, rgb, returnVal=returnVal)
            self.basic.move(returnVal[0], returnVal[1])
            if condition1():
                self.basic.stop()
                return
