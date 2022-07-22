class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def pid(self, error, integral, lasterror, change=1):
        integral += error
        derivative = error - lasterror
        lasterror=error
        speed = (derivative * self.kd * change) + (error * self.kp * change) + (integral * self.ki * change)
        return [speed, integral, lasterror]