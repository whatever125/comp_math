import math


class Result:
    error_message = ""
    has_discontinuity = False
    eps = None

    @staticmethod
    def first_function(x: float):
        return 1 / x

    @staticmethod
    def second_function(x: float):
        if x == 0:
            return (math.sin(Result.eps) / Result.eps + math.sin(-Result.eps) / -Result.eps) / 2
        return math.sin(x) / x

    @staticmethod
    def third_function(x: float):
        return x * x + 2

    @staticmethod
    def fourth_function(x: float):
        return 2 * x + 2

    @staticmethod
    def five_function(x: float):
        return math.log(x)

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
        elif n == 5:
            return Result.five_function
        else:
            raise NotImplementedError(f"Function {n} not defined.")

    @staticmethod
    def calculate_integral(a, b, f_number, epsilon):
        if a > b:
            return -Result.calculate_integral(b, a, f_number, epsilon)

        Result.eps = epsilon
        func = Result.get_function(f_number)
        step = min(epsilon, b - a)
        n = math.ceil((b - a) / step)
        result = 0

        for i in range(n):
            x = a + i * step + step / 2
            try:
                f = func(x)
            except ZeroDivisionError:
                f1 = func(x - epsilon)
                f2 = func(x + epsilon)
                if abs(f1 - f2) <= epsilon:
                    f = f1
                else:
                    Result.has_discontinuity = True
                    Result.error_message = "Integrated function has discontinuity or does not defined in current interval"
                    return None
            except ValueError:
                Result.has_discontinuity = True
                Result.error_message = "Integrated function has discontinuity or does not defined in current interval"
                return None

            result += step * f

        return result


if __name__ == '__main__':
    a = float(input().strip())
    b = float(input().strip())
    f = int(input().strip())
    epsilon = float(input().strip())
    result = Result.calculate_integral(a, b, f, epsilon)
    if not Result.has_discontinuity:
        print(str(result) + '\n')
    else:
        print(Result.error_message + '\n')
    print()
