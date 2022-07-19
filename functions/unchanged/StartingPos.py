class StartingPos():
    RIGHT = 1
    LEFT = -1

    def __int__(self):
        return int('{0}'.format(self.value))

    def neg(self, number):
        return self.int() * value