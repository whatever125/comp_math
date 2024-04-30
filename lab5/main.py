import math


class Result:
    @staticmethod
    def first_function(x: float, y: float):
        return math.sin(x)

    @staticmethod
    def second_function(x: float, y: float):
        return (x * y) / 2

    @staticmethod
    def third_function(x: float, y: float):
        return y - (2 * x) / y

    @staticmethod
    def fourth_function(x: float, y: float):
        return x + y

    @staticmethod
    def default_function(x: float, y: float):
        return 0.0

    @staticmethod
    def get_function(n: int):
        if n == 1:
            return Result.first_function
        elif n == 2:
            return Result.second_function
        elif n == 3:
            return Result.third_function
        elif n == 4:
            return Result.fourth_function
        else:
            return Result.default_function

    @staticmethod
    def solveByAdams(f_num, epsilon, a, y_a, b):
        func = Result.get_function(f_num)
        n = math.ceil((b - a) / epsilon)
        h = (b - a) / n
        y = y_a
        values = [y_a, None, None, None]

        for i in range(3):
            x = a + i * h
            k1 = h * func(x, y)
            k2 = h * func(x + h / 2, y + k1 / 2)
            k3 = h * func(x + h / 2, y + k2 / 2)
            k4 = h * func(x + h, y + k3)
            dy = (k1 + 2 * k2 + 2 * k3 + k4) / 6
            y = y + dy
            values[i + 1] = y

        for i in range(3, n):
            x = a + i * h
            y = y + (55 * func(x, values[-1]) - 59 * func(x - h, values[-2]) + 37 * func(x - 2 * h, values[-3]) - 9 * func(x - 3 * h, values[-4])) * h / 24
            values.pop(0)
            values.append(y)

        return y


if __name__ == '__main__':
    f = int(input().strip())
    epsilon = float(input().strip())
    a = float(input().strip())
    y_a = float(input().strip())
    b = float(input().strip())
    result = Result.solveByAdams(f, epsilon, a, y_a, b)
    print(str(result) + '\n')
