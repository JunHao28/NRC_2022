class Colour:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

class Colours:

    def __init__(self, basic):
        self.basic = basic

        self.blue_floor = Colour("blue_floor", lambda: (basic.sense(1)[0] < 10 and basic.sense(1)[1] < 30 and basic.sense(1)[2] > 30))
        self.brown_floor = Colour("brown_floor", lambda: (basic.sense(1)[0] > 15 and basic.sense(1)[1] < 15 and basic.sense(1)[2] < 15))
        self.green_floor = Colour("green_floor", lambda: (basic.sense(1)[0] > 15 or basic.sense(1)[1] < 30 or basic.sense(1)[2] > 20))
        self.red_floor = Colour("red_floor", lambda: (basic.sense(1)[0] < 40 or basic.sense(1)[1] > 20 or basic.sense(1)[2] > 20))
        
        self.chemical = Colour("chemical", lambda val: val[2] > 10 and sum(val) > 130 and val[0] - val[1] < 5 and val[0] - val[1] > -5 and val[1] - val[2] < 5 and val[1] - val[2] > -5)
        self.fire = Colour("fire", lambda val: val[0] >= 50 and val[1] <= 50 and val[2] <= 50)
        self.human = Colour("human", lambda val: sum(val) > 250)

    def check(self, name):
        colour = "self." + name + ".condition()"
        return exec(colour)

        
    
    
    
