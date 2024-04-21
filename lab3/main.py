import math

k = 0.4
a = 0.9


def first_function(args: []) -> float:
    return math.sin(args[0])


def second_function(args: []) -> float:
    return (args[0] * args[1]) / 2


def third_function(args: []) -> float:
    return math.tan(args[0] * args[1] + k) - pow(args[0], 2)


def fourth_function(args: []) -> float:
    return a * pow(args[0], 2) + 2 * pow(args[1], 2) - 1


def fifth_function(args: []) -> float:
    return pow(args[0], 2) + pow(args[1], 2) + pow(args[2], 2) - 1


def six_function(args: []) -> float:
    return 2 * pow(args[0], 2) + pow(args[1], 2) - 4 * args[2]


def seven_function(args: []) -> float:
    return 3 * pow(args[0], 2) - 4 * args[1] + pow(args[2], 2)


def default_function(args: []) -> float:
    return 0.0


def get_functions(n: int):
    if n == 1:
        return [first_function, second_function]
    elif n == 2:
        k = 0.4
        a = 0.9
        return [third_function, fourth_function]
    elif n == 3:
        k = 0
        a = 0.5
        return [third_function, fourth_function]
    elif n == 4:
        return [fifth_function, six_function, seven_function]
    else:
        return [default_function]


EPSILON = 1e-10


def derivative(f, num: int, args: []):
    delta = EPSILON
    return (f([*args[:num], args[num] + delta, *args[num + 1:]]) -
            f([*args[:num], args[num] - delta, *args[num + 1:]])) / (2 * delta)


def get_triangle_form(matrix, epsilon):
    triangle_matrix = [row[:] for row in matrix]
    count_permutations = 0
    n = len(matrix)
    for i in range(n - 1):
        for j in range(n - 1, i, -1):
            if triangle_matrix[j][i] == 0:
                continue
            else:
                try:
                    ratio = triangle_matrix[j][i] / triangle_matrix[j - 1][i]
                except ZeroDivisionError:
                    triangle_matrix[j], triangle_matrix[j - 1] = (
                        triangle_matrix[j - 1], triangle_matrix[j])
                    count_permutations += 1
                    continue
                for k in range(len(triangle_matrix[j])):
                    triangle_matrix[j][k] = (triangle_matrix[j][k] -
                                             ratio * triangle_matrix[j - 1][k])
                    if abs(triangle_matrix[j][k]) < epsilon ** 2:
                        triangle_matrix[j][k] = 0
    return triangle_matrix, count_permutations


def count_determinant(matrix):
    determinant = 1
    triangle_matrix, count_permutations = get_triangle_form(matrix, EPSILON)
    for i in range(len(matrix)):
        determinant *= triangle_matrix[i][i]
    return determinant * (-1) ** (count_permutations != 0)


def get_transposed_matrix(matrix):
    return list(map(lambda x: list(x), zip(*matrix)))


def get_matrix_minor(matrix, i, j):
    return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]


def get_regularized_matrix(matrix, regularization_param):
    modified_matrix = [[matrix[i][j] + regularization_param if i == j else matrix[i][j] for j in range(len(matrix[0]))]
                       for i in range(len(matrix))]
    return modified_matrix


def get_inverse_matrix(matrix):
    determinant = count_determinant(matrix)
    print(determinant)
    if determinant == 0:
        determinant = 10
        # return get_inverse_matrix(get_regularized_matrix(matrix, 1))
    if len(matrix) == 2:
        return [[matrix[1][1] / determinant, -matrix[0][1] / determinant],
                [-matrix[1][0] / determinant, matrix[0][0] / determinant]]

    cofactors = []
    for r in range(len(matrix)):
        cofactor_row = []
        for c in range(len(matrix)):
            minor = get_matrix_minor(matrix, r, c)
            cofactor_row.append(((-1) ** (r + c)) * count_determinant(minor))
        cofactors.append(cofactor_row)
    cofactors = get_transposed_matrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    return cofactors


def multiply_matrix_by_matrix(matrix_a, matrix_b):
    if len(matrix_a[0]) != len(matrix_b):
        return None
    transposed_b = get_transposed_matrix(matrix_b)
    return [[sum(el_a * el_b for el_a, el_b in zip(row_a, col_b))
             for col_b in transposed_b] for row_a in matrix_a]


def multiply_matrix_by_vector(matrix, vector):
    if len(matrix[0]) != len(vector):
        return None
    result_vector = []
    for i in range(len(matrix[0])):
        summ = 0
        for j in range(len(vector)):
            summ += vector[j] * matrix[i][j]
        result_vector.append(summ)
    return result_vector


def distance(a, b):
    return math.sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(a, b)]))


def solve_by_fixed_point_iterations(system_id, number_of_unknowns, initial_approximations):
    system = get_functions(system_id)
    X = initial_approximations
    while True:
        X_old = X.copy()
        F = [f(X_old) for f in system]
        W = [[derivative(system[i], j, X) for j in range(number_of_unknowns)] for i in range(len(system))]
        W_inverse = get_inverse_matrix(W)
        P = multiply_matrix_by_vector(W_inverse, F)
        X = [X_old[i] - P[i] for i in range(len(X))]
        if distance(X, X_old) < EPSILON:
            break

    return X


if __name__ == '__main__':
    system_id = int(input().strip())

    number_of_unknowns = int(input().strip())

    initial_approximations = []

    for _ in range(number_of_unknowns):
        initial_approximations_item = float(input().strip())
        initial_approximations.append(initial_approximations_item)

    result = solve_by_fixed_point_iterations(system_id, number_of_unknowns, initial_approximations)

    print('\n'.join(map(str, result)))
    print('\n')
