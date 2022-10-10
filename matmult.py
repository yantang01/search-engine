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


def euclidean_dist(a, b):
    total = 0

    # single row, row number == 0
    # n means how many columns in both matrix_a and matrix_b
    for n in range(len(a[0])):
        # based on formula
        total += ((a[0][n] - b[0][n])**2)

    # return root of total
    return total**0.5
