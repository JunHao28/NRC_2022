
class Robot:

    forwardki = 1
    forwardkp = 1
    forwardkd = 1
    gyroki = 1
    gyrokp = 1
    gyrokd = 1
    
    def __init__(self, ev3, motors, sensors):
        self.ev3 = ev3
        self.motors = motors
        self.sensors = sensors

    def beep(): 
        ev3.speaker.beep()

    def move(leftspeed, rightspeed):
        motors.motorb.run(leftspeed)
        motors.motorc.run(rightspeed)

    def pidmovedistance(degree, speed):
        currentAngle = motor.motora.angle()
        integral = 0
        derivative = 0
        last_error = 0
        while degree < currentAngle:
            error = degree + currentAngle - motor.motora.angle()
            integral = integral + error
            derivative = error - last_error
            speed = (derivative * forwardkd) + (error * forwardkp) + (integral * forwardki)
            last_error = error
            Robot.move(speed, speed)
    
    def pidmovegyrodegree(degree, speed):
        currentAngle = motor.motora.angle()
        currentDegree = sensor1.angle()
        distanceIntegral = 0
        distanceDerivative = 0
        distanceLast_error = 0
        gyroIntegral = 0
        gyroDerivative = 0
        gyroLast_error = 0
        while degree < currentAngle:
            distanceError = degree + currentAngle - motor.motora.angle()
            distanceIntegral = distanceIntegral + distanceError
            distanceDerivative = distanceError - distanceLastError
            speed = (distanceDerivative * forwardkd) + (distanceError * forwardkp) + (distanceIntegral * forwardki)
            distanceLastError = distanceError
            gyroError = currentDegree - sensor1.angle()
            gyroIntegral = gyroIntegral + distanceError
            gyroDerivative = gyroError - gyroLastError
            gyroLastError = gyroError
            leftspeed = speed + (distanceDerivative * forwardkd) + (distanceError * forwardkp) + (distanceIntegral * forwardki)
            rightspeed = speed - (distanceDerivative * forwardkd) + (distanceError * forwardkp) + (distanceIntegral * forwardki)

            

            

class Motors:
    def __init__(self, motora, motorb, motorc, motord):
        self.motora = motora,
        self.motorb = motorb,
        self.motorc = motorc,
        self.motord = motord,

class Sensors: 
    def __init__(self, sensor1, sensor2, sensor3, sensor4):
        self.sensor1 = sensor1,
        self.sensor2 = sensor2,
        self.sensor3 = sensor3,
        self.sensor4 = sensor4,

class BaseSpeed:
    def __init__(self, leftBase, rightBase):
        self.leftBase = leftBase,
        self.rightBase  rightBase,