import math


class Result:
    isMethodApplicable = True
    errorMessage = ""

    @staticmethod
    def get_triangle_form(n, matrix, epsilon):
        triangle_matrix = [row[:] for row in matrix]
        count_permutations = 0
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

    @staticmethod
    def count_determinant(n, matrix, epsilon):
        determinant = 1
        triangle_matrix, count_permutations = Result.get_triangle_form(n, matrix, epsilon)
        for i in range(n):
            determinant *= triangle_matrix[i][i]
        return determinant * (-1) ** (count_permutations != 0)

    @staticmethod
    def get_transposed_matrix(matrix):
        return list(map(lambda x: list(x), zip(*matrix)))

    @staticmethod
    def get_matrix_minor(matrix, i, j):
        return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]

    @staticmethod
    def get_inverse_matrix(n, matrix, epsilon):
        determinant = Result.count_determinant(n, matrix, epsilon)
        # special case for 2x2 matrix:
        if len(matrix) == 2:
            return [[matrix[1][1] / determinant, -matrix[0][1] / determinant],
                    [-matrix[1][0] / determinant, matrix[0][0] / determinant]]

        # find matrix of cofactors
        cofactors = []
        for r in range(len(matrix)):
            cofactor_row = []
            for c in range(len(matrix)):
                minor = Result.get_matrix_minor(matrix, r, c)
                cofactor_row.append(((-1) ** (r + c)) *
                                    Result.count_determinant(len(minor), minor, epsilon))
            cofactors.append(cofactor_row)
        cofactors = Result.get_transposed_matrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c] / determinant
        return cofactors

    @staticmethod
    def multiply_matrix_by_matrix(matrix_a, matrix_b):
        if len(matrix_a[0]) != len(matrix_b):
            return None
        transposed_b = Result.get_transposed_matrix(matrix_b)
        return [[sum(el_a * el_b for el_a, el_b in zip(row_a, col_b))
                 for col_b in transposed_b] for row_a in matrix_a]

    @staticmethod
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

    @staticmethod
    def solveBySimpleIterations(n, matrix, epsilon):
        # Check if incorrect matrix
        if n != len(matrix) or any(map(lambda row: len(row) != n + 1, matrix)):
            Result.errorMessage = "The system is invalid"
            Result.isMethodApplicable = False
            return None

        # Check if determinant == 0
        if Result.count_determinant(n, matrix, epsilon) == 0:
            Result.errorMessage = "The system has determinant equal to zero"
            Result.isMethodApplicable = False
            return None

        A = list(map(lambda row: row[:-1], matrix))
        b = list(map(lambda row: row[-1], matrix))
        D = [[n if i == j else 1 for j in range(n)] for i in range(n)]
        A_inversed = Result.get_inverse_matrix(n, A, epsilon)
        B = Result.multiply_matrix_by_matrix(D, A_inversed)
        d = Result.multiply_matrix_by_vector(B, b)

        # Diagonal dominant matrix
        new_matrix = list(zip(*D, d))

        # Check if matrix is not diagonal dominant
        if any(abs(new_matrix[i][i]) < sum(abs(new_matrix[i][j]) if j != i else 0
                                           for j in range(n)) for i in range(len(new_matrix))):
            Result.errorMessage = ("The system has no diagonal dominance for this method. "
                                   "Method of the simple iterations is not applicable.")
            Result.isMethodApplicable = False
            return None

        prev_x_vector = [math.inf] * len(new_matrix)
        x_vector = [0] * len(new_matrix)

        while any(abs(x_vector[i] - prev_x_vector[i]) > epsilon for i in range(n)):
            prev_x_vector = x_vector
            x_vector = [
                prev_x_vector[i] - (sum([new_matrix[i][j] * prev_x_vector[j] for j in range(n)]) - new_matrix[i][-1]) /
                new_matrix[i][i] for i in range(n)]

        return x_vector


if __name__ == '__main__':

    n = int(input().strip())

    matrix_rows = n
    matrix_columns = n + 1

    matrix = []

    for _ in range(matrix_rows):
        matrix.append(list(map(float, input().rstrip().split())))

    epsilon = float(input().strip())

    result = Result.solveBySimpleIterations(n, matrix, epsilon)
    if Result.isMethodApplicable:
        print('\n'.join(map(str, result)))
    else:
        print(f"{Result.errorMessage}")
