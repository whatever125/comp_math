import math


def approximate_sigmoid(x_axis, y_axis):
    if len(x_axis) < 3 or len(y_axis) < 3 or len(x_axis) != len(y_axis):
        return 0

    def approximate(x):
        result_sum = y_axis[0] * sigmoid(x - x_axis[0])
        for i in range(1, len(x_axis)):
            result_sum += (y_axis[i] - y_axis[i - 1]) * sigmoid(x - (x_axis[i] + x_axis[i - 1]) / 2) / 2
        return result_sum

    errors = []
    for (x, y) in zip(x_axis, y_axis):
        errors.append(abs(approximate(x) - y))
    return max(errors)


def sigmoid(x):
    return math.tanh(x)


if __name__ == '__main__':
    axis_count = int(input().strip())

    x_axis = list(map(float, input().rstrip().split()))

    y_axis = list(map(float, input().rstrip().split()))

    result = approximate_sigmoid(x_axis, y_axis)

    print(str(result) + '\n')
