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


def check_directory(dir_name):
    if os.path.isdir(dir_name):
        return True
    else:
        return False


def read_file(dirname, filename):
    file_path = os.path.join(dirname, filename)
    f = open(file_path, "r")
    data = f.read()
    js = json.loads(data)
    f.close()
    return js


def write_to_file(dirname, filename, content):
    file_path = os.path.join(dirname, filename)
    fileout = open(file_path, "w")
    fileout.write(json.dumps(content))
    fileout.close()


def ID_to_URL(ID):
    URL_mapping = read_file("data", "map_id_to_url.txt")

    return URL_mapping[str(ID)]


def URL_to_ID(URL):
    ID_mapping = read_file("data", "links_visited.txt")

    return ID_mapping[URL]


def get_matrix_value(ID, outgoing_ID):
    URL = ID_to_URL(ID)
    outgoing_URL = ID_to_URL(outgoing_ID)
    if outgoing_URL in get_outgoing_links(URL):
        return True
    else:
        return False


# O(1) time complexity --> read data from file
def get_outgoing_links(URL):  # PASSED TEST
    dirname = get_dirname(URL)
    if check_directory(dirname) == False:
        return None
    outgoing_links = read_file(dirname, "outgoing_links.txt")
    return outgoing_links


# O(1) time complexity --> read data from file
def get_incoming_links(URL):  # PASSED TEST
    dirname = get_dirname(URL)
    if check_directory(dirname) == False:
        return None
    incoming_links = read_file(dirname, "incoming_links.txt")
    return incoming_links


def write_page_rank_to_files(URL):  # PASSED TEST
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
    # 4. Scaled Adjacency Matrix; alpha value of 0.1
    # 5. Adjacency Matrix after adding alpha/N to each entry
    for r in range(ROWS):
        for c in range(COLS):
            matrix[r][c] = ((matrix[r][c] / counter[r]) * 0.9) + (0.1/ROWS)

    # matrix = matmult.mult_scalar(matrix, 0.9)

    # for r in range(ROWS):
    #     for c in range(COLS):
    #         matrix[r][c] = matrix[r][c] + (0.1/ROWS)

    # 6. Multiply the matrix by a vector
    distance = 99
    vector = [[1/ROWS] * ROWS]
    while distance > 0.0001:
        new_vector = matmult.mult_matrix_test(vector, matrix)
        distance = matmult.euclidean_dist(vector, new_vector)
        vector = new_vector

    for link in links_visited:
        dirname = get_dirname(link)
        ID = URL_to_ID(link)
        write_to_file(dirname, "page_rank.txt", vector[0][ID])


def get_page_rank(URL):
    dirname = get_dirname(URL)

    if check_directory(dirname) == False:
        return -1

    return read_file(dirname, "page_rank.txt")


# Term Frequencies
# read --> O(1)
def get_tf(URL, word):
    dirname = get_dirname(URL)

    if check_directory(dirname) == False:
        return 0

    tf = read_file(dirname, "tf.txt")

    if word not in tf:
        return 0

    return tf[word]


# IDFs
def get_idf(word):  # PASSED TEST
    idf = read_file("data", "idf.txt")

    if word not in idf:
        return 0

    return idf[word]


# tf-idfs
def get_tf_idf(URL, word):  # PASSED TEST
    dirname = get_dirname(URL)

    if check_directory(dirname) == False:
        return 0

    tfidf = read_file(dirname, "tf-idfs.txt")

    if word not in tfidf:
        return 0

    return tfidf[word]


def get_tf_query_word(query, word):
    query = query.split(" ")
    # coconut fig peach papaya kiwi kiwi
    counter = {}
    for w in query:
        if w in counter:
            counter[w] += 1
        else:
            counter[w] = 1
    return counter[word] / len(query)


def get_idf_query_word(word):
    idfs = read_file("data", "idf.txt")
    if word not in idfs:
        return 0
    return idfs[word]
