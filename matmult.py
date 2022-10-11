from turtle import distance


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


def mult_matrix(a, b):
    # invalid input --> if number of cols in matrix_a != number of rows in matrix_b, then matrix_a cannot multiply matrix_b
    if len(a[0]) != len(b):
        return None

    result = []

    # loop through matrix_a rows
    for a_row in range(len(a)):
        row = []
        # loop through matrix_b columns
        for b_col in range(len(b[0])):
            total = 0
            # n --> how many times of multiplication; n should == number of columns in matrix_a or number of rows in matrix_b
            for n in range(len(a[0])):
                total += a[a_row][n] * b[n][b_col]

            row.append(total)

        result.append(row)

    return result


def mult_matrix_test(matrix1, matrix2):
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


# vector = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]
# matrix = [
#     [0.01, 0.1225, 0.1225, 0.1225, 0.1225, 0.1225, 0.1225, 0.1225, 0.1225, 0.01],
#     [0.46, 0.01, 0.46, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#     [0.31, 0.31, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.31, 0.01],
#     [0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#     [0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#     [0.31, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.31, 0.31],
#     [0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#     [0.91, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
#     [0.31, 0.01, 0.31, 0.01, 0.01, 0.31, 0.01, 0.01, 0.01, 0.01],
#     [0.01, 0.01, 0.01, 0.01, 0.01, 0.91, 0.01, 0.01, 0.01, 0.01],
# ]

# res = []
# calculation = []

# for c in range(len(matrix[0])):
#     col_sum = 0
#     for r in range(len(matrix)):
#         col_sum += matrix[r][c]
#     calculation.append(col_sum * vector[0][0])
# res.append(calculation)

# print(res)

# # matrix[0][0] + matrix[1][0] + matrix[2][0]
# # element = 0.1 * (0.01+0.46+...+0.01)
# # calculation.append(element)


# # print(mult_matrix_test(vector, matrix))

# # new_vector = mult_matrix_test(vector, matrix)
# # distance = euclidean_dist(vector, new_vector)

# # print(new_vector)
# # print(distance)


# def getColAsList(matrixToManipulate, col):
#     myList = []
#     numOfRows = len(matrixToManipulate)
#     for i in range(numOfRows):
#         myList.append(matrixToManipulate[i][col])
#     return myList


# def getCell(matrix1, matrix2, r, c):
#     matrixBCol = getColAsList(matrix2, c)
#     lenOfList = len(matrixBCol)
#     productList = [matrix1[r][i]*matrixBCol[i] for i in range(lenOfList)]
#     return sum(productList)


# def mult_matrix_test_version2(matrix1, matrix2):
#     res = [[0 for x in range(len(matrix1))for y in range(len(matrix2[0]))]]

#     if (len(matrix1[0]) != len(matrix2)):
#         return None

#     for i in range(len(matrix1)):
#         for j in range(len(matrix2[0])):
#             res[i][j] = getCell(matrix1, matrix2, i, j)
#         print(res[i])
