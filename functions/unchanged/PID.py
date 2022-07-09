class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def pid(self, error, integral, lasterror):
        integral += error
        derivative = error - lasterror
        lasterror=error
        speed = (derivative * self.kd) + (error * self.kp) + (integral * self.ki)
        return [speed, integral, lasterror]