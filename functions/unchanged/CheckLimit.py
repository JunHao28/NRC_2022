class CheckLimit:
    def maximum(number: int, maximum: int):
        if number <= maximum:
            return number
        else:
            return maximum

    def minimum(number: int, minimum: int):
        if number >= minimum:
            return number
        else:
            return minimum

    def minimaximum(number: int, minimum: int, maximum: int):
        if number < 0:
            minimum1 = minimum
            maximum1 = maximum
            minimum = -maximum1
            maximum = -minimum1
        return int(CheckLimit.minimum(CheckLimit.maximum(number, maximum), minimum))