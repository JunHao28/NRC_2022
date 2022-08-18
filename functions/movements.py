import time
from pybricks.parameters import Port, Stop, Direction, Button, Color
from functions.unchanged.PID import PID
from functions.unchanged.CheckLimit import CheckLimit


#robot.beep() (beep)
# robot.turn(speed, degree, oneWheel=0) (turning, oneWheel: (0, two wheel) (1, rightwheel) (2, leftwheel))

class Movement:

    # PID values
    gyros = PID(90, 0, 10)
    oneWheelTurn = PID(15, 0.000000025, 8)
    twoWheelTurn = PID(7.5, 0.000000025, 4)
    track = PID(1.3, 0, 5)

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
                right = -result[0] if (oneWheel != 1) else 0
                left = result[0] if (oneWheel != 2) else 0
                self.basic.move(left, right)

    def decelerate(self, degree, accelDist=40, deccelDist=200, maximumSpeed=1500, minimumSpeed=20, move=True, currentAngle=0):
        if move:
            currentAngle = self.motorb.angle()
            result = [0, 0, 1000]
        finalAngle = abs(self.motorb.angle()-currentAngle)
        degree = abs(degree)
        while finalAngle < degree:
            if finalAngle < accelDist:
                speed = minimumSpeed + (maximumSpeed - minimumSpeed) * (finalAngle / accelDist)
            elif finalAngle > degree - deccelDist:
                speed = minimumSpeed + (maximumSpeed - minimumSpeed) * ((degree - finalAngle) / deccelDist/4)
            else: 
                speed = maximumSpeed
            if move:
                self.basic.move(speed, speed)
            else:
                return speed
            finalAngle = abs(self.motorb.angle()-currentAngle)
        self.basic.stop()
        return None

    def gyro(self, speed=700, condition=None, minimumSpeed=0, override=None, inputs=None):
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

    def gyrodegree(self, speed, degree, minimumSpeed=20, maximumSpeed=1500, override=None):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        if override != None:
            currentDegree = override
        output = [0, 1000, 0, 0]
        while True:
            pidDistance = self.decelerate(
                degree, minimumSpeed=minimumSpeed, maximumSpeed=maximumSpeed, move=False, currentAngle=currentAngle)
            if pidDistance == None:
                break
            output = self.gyro(speed=900, minimumSpeed=minimumSpeed, inputs=[
                               output[0], output[1], currentDegree], override=override)
            left = CheckLimit.minimaximum(output[2]*0.8+pidDistance*0.4, minimumSpeed, 1500)
            right = CheckLimit.minimaximum(output[3]*0.8+pidDistance*0.4, minimumSpeed, 1500)
            self.basic.move(left, right) if degree > 0 else self.basic.move(-right, -left)
        self.basic.stop()

    def gyroTillSense(self, speed, condition, minimumSpeed=20, stopAfter=None, override=None):
        currentAngle = self.motorb.angle()
        currentDegree = self.sensor1.angle()
        outputs = [0, 0]
        if override != None:
            currentDegree = override
        while True:
            output = self.gyro(speed=speed, minimumSpeed=minimumSpeed, inputs=[
                outputs[0], outputs[1], currentDegree], override=override)
            self.basic.move(output[2], output[3])
            if condition() or (stopAfter != None and (abs(stopAfter) <= abs(self.motorb.angle()-currentAngle))):
                self.basic.stop()                
                self.basic.beep()  
                return None
        return

    def pidLineTracking(self, rgb, speed, returnVal=None):
        result = [0, 0, 0]
        if returnVal != None:
            result = returnVal
        while True:
            error = self.sensor2.reflection() - rgb
            result = self.track.pid(error, result[1], result[2], change=1)
            change = CheckLimit.maximum(result[0], 1500-speed)
            if returnVal == None:
                self.basic.move(-speed + change, - speed - change)
            else:
                return [-speed + change, - speed - change, result[1], result[2]]
        self.basic.stop()

    def lineTrackingTillSense(self, rgb, speed, condition):
        returnVal = [0, 0, 0, 0]
        while True:
            returnVal = self.pidLineTracking(rgb, speed, returnVal=[0, returnVal[2], returnVal[3]])
            self.basic.move(returnVal[0], returnVal[1])
            if condition():
                self.basic.stop()
                return
