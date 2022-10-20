import os
import global_functions


# O(1) time complexity --> read data from file
def get_outgoing_links(URL):  # PASSED TEST
    dirname = global_functions.get_dirname(URL)
    if not os.path.isdir(dirname):
        return None
    outgoing_links = global_functions.read_file(dirname, "outgoing_links.txt")
    return outgoing_links


# O(1) time complexity --> read data from file
def get_incoming_links(URL):  # PASSED TEST
    dirname = global_functions.get_dirname(URL)
    if not os.path.isdir(dirname):
        return None
    incoming_links = global_functions.read_file(dirname, "incoming_links.txt")
    return incoming_links


# def write_page_rank_to_files(URL):  # PASSED TEST
#     links_visited = global_functions.read_file("data", "links_visited.txt")
#     if URL not in links_visited:
#         return -1

#     # 1. Generate Matrix
#     ROWS = COLS = global_functions.read_file("data", "length.txt")
#     matrix = [[0] * COLS for i in range(ROWS)]

#     # count 1s
#     counter = []

#     # 2. Adjacency Matrix
#     for r in range(ROWS):
#         count = 0
#         for c in range(COLS):
#             if get_matrix_value(r, c) == False:
#                 continue
#             matrix[r][c] = 1  # r is the page ID, c is the outgoing links' ID
#             count += 1
#         counter.append(count)

#     # 3. Initial transition
#     # 4. Scaled Adjacency Matrix; alpha value of 0.1
#     # 5. Adjacency Matrix after adding alpha/N to each entry
#     for r in range(ROWS):
#         for c in range(COLS):
#             matrix[r][c] = ((matrix[r][c] / counter[r]) * 0.9) + (0.1/ROWS)

#     # matrix = matmult.mult_scalar(matrix, 0.9)

#     # for r in range(ROWS):
#     #     for c in range(COLS):
#     #         matrix[r][c] = matrix[r][c] + (0.1/ROWS)

#     # 6. Multiply the matrix by a vector
#     distance = 99
#     vector = [[1/ROWS] * ROWS]
#     while distance > 0.0001:
#         new_vector = matmult.mult_matrix_test(vector, matrix)
#         distance = matmult.euclidean_dist(vector, new_vector)
#         vector = new_vector

#     for link in links_visited:
#         dirname = global_functions.get_dirname(link)
#         ID = URL_to_ID(link)
#         global_functions.write_to_file(dirname, "page_rank.txt", vector[0][ID])


def get_page_rank(URL):
    dirname = global_functions.get_dirname(URL)

    if not os.path.isdir(dirname):
        return -1

    return global_functions.read_file(dirname, "page_rank.txt")


# Term Frequencies
# read --> O(1)
def get_tf(URL, word):
    dirname = global_functions.get_dirname(URL)

    if not os.path.isdir(dirname):
        return 0

    tf = global_functions.read_file(dirname, "tf.txt")

    if word not in tf:
        return 0

    return tf[word]


# IDFs
def get_idf(word):  # PASSED TEST
    idf = global_functions.read_file("data", "idf.txt")

    if word not in idf:
        return 0

    return idf[word]


# tf-idfs
def get_tf_idf(URL, word):  # PASSED TEST
    dirname = global_functions.get_dirname(URL)

    if not os.path.isdir(dirname):
        return 0

    tfidf = global_functions.read_file(dirname, "tf-idfs.txt")

    if word not in tfidf:
        return 0

    return tfidf[word]
