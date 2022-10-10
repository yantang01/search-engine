import json
import os
import math
import matmult


def get_dirname(full):
    start = full.rfind("/")
    end = full.rfind(".html")
    dirname = full[start + 1:end]
    file_path = os.path.join("data", dirname)
    return file_path


def read_file(dirname, filename):
    file_path = os.path.join(dirname, filename)
    f = open(file_path, "r")
    data = f.read()
    js = json.loads(data)
    f.close()
    return js


def ID_to_URL(ID):
    ID_mapping = read_file("data", "links_visited.txt")
    for k in ID_mapping:
        if ID_mapping[k] == ID:
            return k


def URL_to_ID(URL):
    ID_mapping = read_file("data", "links_visited.txt")
    for k in ID_mapping:
        if k == URL:
            return ID_mapping[k]


def get_matrix_value(ID, outgoing_ID):
    URL = ID_to_URL(ID)
    outgoing_URL = ID_to_URL(outgoing_ID)
    if outgoing_URL in get_outgoing_links(URL):
        return True
    else:
        return False


def get_outgoing_links(URL):
    dirname = get_dirname(URL)
    outgoing_links = read_file(dirname, "outgoing_links.txt")
    return outgoing_links if outgoing_links else None


def get_incoming_links(URL):
    dirname = get_dirname(URL)
    incoming_links = read_file(dirname, "incoming_links.txt")
    return incoming_links if incoming_links else None


def get_page_rank(URL):
    links_visited = read_file("data", "links_visited.txt")
    if URL not in links_visited:
        return -1

    # 1. Generate Matrix
    ROWS = COLS = read_file("data", "length.txt")
    matrix = [[0] * COLS for i in range(ROWS)]

    # count 1s
    counter = []

    # 2. Adjacency Matrix
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if get_matrix_value(r, c) == False:
                continue
            matrix[r][c] = 1  # r is the page ID, c is the outgoing links' ID
            count += 1
        counter.append(count)

    # 3. Initial transition
    for r in range(ROWS):
        for c in range(COLS):
            matrix[r][c] = matrix[r][c] / counter[r]

    # 4. Scaled Adjacency Matrix
    # alpha value of 0.1
    matrix = matmult.mult_scalar(matrix, 0.9)

    # 5. Adjacency Matrix after adding alpha/N to each entry
    for r in range(ROWS):
        for c in range(COLS):
            matrix[r][c] = matrix[r][c] + (0.1/ROWS)

    # 6. Multiply the matrix by a vector
    distance = 99
    vector = [[1/ROWS] * ROWS]
    while distance > 0.0001:
        new_vector = matmult.mult_matrix(vector, matrix)
        distance = matmult.euclidean_dist(vector, new_vector)
        vector = new_vector

    ID = URL_to_ID(URL)
    return vector[0][ID]


def get_tf(URL, word):
    dirname = get_dirname(URL)
    words = read_file(dirname, "words.txt")
    links_visited = read_file("data", "links_visited.txt")

    if word not in words or URL not in links_visited:
        return 0

    count = 0

    for v in words.values():
        count += v

    return words[word] / count


def get_idf(word):
    links_visited = read_file("data", "links_visited.txt")

    num_of_documents_w = 0
    num_of_documents = 0

    for URL in links_visited:

        num_of_documents += 1

        dirname = get_dirname(URL)
        words = read_file(dirname, "words.txt")
        if word in words:
            num_of_documents_w += 1

    if num_of_documents_w == 0:
        return 0

    return math.log((num_of_documents / (1 + num_of_documents_w)), 2)


def get_tf_idf(URL, word):
    return math.log((1 + get_tf(URL, word)), 2) * get_idf(word)
