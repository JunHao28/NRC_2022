class Basic:
    def __init__(self, ev3, motor, sensor):
        self.ev3 = ev3
        self.motorb = motor[0]
        self.motorc = motor[1]
        self.motord = motor[2]
        self.sensor1 = sensor[0]
        self.sensor2 = sensor[1]
        self.sensor3 = sensor[2]
        self.sensor4 = sensor[3]

    def move(self, leftspeed, rightspeed):
        self.motorb.run(leftspeed)
        self.motorc.run(rightspeed)

    def stop(self):
        self.motorb.hold()
        self.motorc.hold()
        self.motord.hold()

    def beep(self):
        self.ev3.speaker.beep()
    
    def resetRobot(self):
        self.motorb.reset_angle(0)
        self.motorc.reset_angle(0)
        self.motord.reset_angle(0)
        self.sensor1.reset_angle(0)
        self.motorb.control.limits(1500)
        self.motorc.control.limits(1500)
    
    def sense(self, sensorNo):
        sensors = [self.sensor1, self.sensor2, self.sensor3, self.sensor4]
        if sensorNo == 0:
            return sensors[sensorNo].angle()
        elif sensorNo == 1:
            return sensors[sensorNo].rgb()
        else:
            rgb = sensors[sensorNo].read("RGB")
            if sum(rgb) == 0:
                return [0, 0, 0, 0]
            return [rgb[0]/sum(rgb)*100, rgb[1]/sum(rgb)*100, rgb[2]/sum(rgb)*100, rgb[3]/sum(rgb)*100,]
    
    def check(self, sensorNo, rgb, leeway1=10, leeway2=10):
        sensor = self.sense(sensorNo)
        if ((sum(sensor) <= rgb+leeway1) and (sum(sensor) >= rgb-leeway2)):
            return True
        else:
            return False