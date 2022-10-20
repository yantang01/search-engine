def mult_scalar(matrix, scale):
    result = []

    # locate each cell --> multiplied by the scale --> add to new row list
    for r in range(len(matrix)):
        new_row = []
        for c in range(len(matrix[0])):
            new_row.append(matrix[r][c] * scale)

        # add each new row to result
        result.append(new_row)

    return result


def mult_matrix(matrix1, matrix2):

    if len(matrix1[0]) != len(matrix2):
        return None

    res = [[0 for x in range(len(matrix1))for y in range(len(matrix2[0]))]]

    # explicit for loops
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):

                # resulted matrix
                res[i][j] += matrix1[i][k] * matrix2[k][j]

    return res


def euclidean_dist(a, b):
    total = 0

    # single row, row number == 0
    # n means how many columns in both matrix_a and matrix_b
    for n in range(len(a[0])):
        # based on formula
        total += ((a[0][n] - b[0][n])**2)

    # return root of total
    return total**0.5
