class Colour:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

class Colours:

    def __init__(self, basic):
        self.basic = basic

    def check(self, name):
        return name.conditon()

        
    blue_floor = Colour("blue_floor", lambda: (basic.sense(1)[0] < 10 and basic.sense(1)[1] < 30 and basic.sense(1)[2] > 30))
    brown_floor = Colour("brown_floor", lambda: (basic.sense(1)[0] > 15 and basic.sense(1)[1] < 15 and basic.sense(1)[2] < 15))
    green_floor = Colour("green_floor", lambda: (basic.sense(1)[0] > 15 or basic.sense(1)[1] < 30 or basic.sense(1)[2] > 20))
    red_floor = Colour("red_floor", lambda: (basic.sense(1)[0] < 40 or basic.sense(1)[1] > 20 or basic.sense(1)[2] > 20))

    
    
    
