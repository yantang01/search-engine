import math
import os

import global_functions
import matmult
import searchdata
import webdev


def parse_links(contents):
    start_index = 0
    end_index = 0
    start_tag = 'a href="'
    end_tag = '">'
    links = []
    while True:
        # get all the words in a list
        start_index = contents.find(start_tag, end_index)
        if start_index == -1:
            break
        end_index = contents.find(end_tag, start_index)
        # words is a list of all the words
        links.append(
            contents[(len(start_tag) + start_index):end_index])
    return links


def parse_words(contents):
    start_index = 0
    end_index = 0
    start_tag = '<p>'
    end_tag = '</p>'
    while True:
        # get all the words in a list
        start_index = contents.find(start_tag, end_index)
        if start_index == -1:
            break
        end_index = contents.find(end_tag, start_index)
        # words is a list of all the words
        words = contents[(len("<p>") + start_index):end_index].split()

    return words


def get_title(contents):
    start_tag = '<title>'
    end_tag = '</title>'
    start_index = contents.find(start_tag)
    end_index = contents.find(end_tag)
    return contents[(len("<title>") + start_index):end_index]


# helper function to get full url
# if url starts with ./
# combine it with seed url
# else
# use the url
def get_full_url(url, base):
    if url.startswith('./'):
        # add to the seed url
        start = url.find("./")
        end = base.rfind("/")
        full = base[:end] + url[start + 1:]
        return full
    else:
        return url


def create_directory(dirname):
    os.makedirs(dirname)


def create_file(dirname, filename):
    file_path = os.path.join(dirname, filename)
    fileout = open(file_path, "w")
    fileout.close()


def delete_files():
    os.system("rm -rf data")


def setup_files(dir_name):
    create_directory(dir_name)
    create_file(dir_name, "title.txt")
    create_file(dir_name, "incoming_links.txt")
    create_file(dir_name, "outgoing_links.txt")
    create_file(dir_name, "page_rank.txt")
    create_file(dir_name, "tf.txt")
    create_file(dir_name, "tf-idfs.txt")


def write_idf_to_file(links_visited, word_appears):
    idf = {}
    num_of_docs = len(links_visited)
    for w in word_appears:
        idf[w] = math.log((num_of_docs / (1+(len(word_appears[w])))), 2)
    global_functions.write_to_file("data", "idf.txt", idf)


def write_tfidf_to_files(links_visited):

    idf = global_functions.read_file("data", "idf.txt")

    for link in links_visited:
        tfidf = {}
        dirname = global_functions.get_dirname(link)
        tf = global_functions.read_file(dirname, "tf.txt")
        for w in tf:
            tfidf[w] = math.log((1 + tf[w]), 2) * idf[w]

        global_functions.write_to_file(dirname, "tf-idfs.txt", tfidf)


def write_incoming_links_to_files(incoming_links):
    for key in incoming_links:
        global_functions.write_to_file(global_functions.get_dirname(key), "incoming_links.txt",
                                       incoming_links[key])


def ID_to_URL(ID, URL_mapping):

    return URL_mapping[ID]


def URL_to_ID(URL, ID_mapping):

    return ID_mapping[URL]


def get_matrix_value(ID, outgoing_ID, map_ID_to_URL):
    URL = ID_to_URL(ID, map_ID_to_URL)
    outgoing_URL = ID_to_URL(outgoing_ID, map_ID_to_URL)
    if outgoing_URL in searchdata.get_outgoing_links(URL):
        return True
    else:
        return False


def write_page_rank_to_files(URL, links_visited, map_ID_to_URL):  # PASSED TEST
    # links_visited = global_functions.read_file("data", "links_visited.txt")
    if URL not in links_visited:
        return -1

    # 1. Generate Matrix
    ROWS = COLS = len(links_visited)
    matrix = [[0] * COLS for i in range(ROWS)]

    # count 1s
    counter = []

    # 2. Adjacency Matrix
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if get_matrix_value(r, c, map_ID_to_URL) == False:
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
        dirname = global_functions.get_dirname(link)
        ID = URL_to_ID(link, links_visited)
        global_functions.write_to_file(dirname, "page_rank.txt", vector[0][ID])


def crawl(seed):
    delete_files()

    incoming_links = {}
    word_appears = {}

    queue = [seed]
    links_visited = {}
    map_ID_to_URL = {}
    ID = 0
    links_visited[seed] = ID
    map_ID_to_URL[ID] = seed

    # while queue is not empty
    while queue:
        # read the top URL
        contents = webdev.read_url(queue[0])

        # set up file structures
        dirname = global_functions.get_dirname(queue[0])
        setup_files(dirname)

        # write title to title.txt
        global_functions.write_to_file(
            dirname, "title.txt", get_title(contents))

        # return a list of words in one page
        words = parse_words(contents)
        tf = {}

        # add words in the all_words dictionary
        for w in words:

            if w not in tf:
                tf[w] = (1 / len(words))
            else:
                tf[w] += (1 / len(words))

            if w not in word_appears:
                word_appears[w] = [queue[0]]
            else:
                if queue[0] in word_appears[w]:
                    continue
                else:
                    word_appears[w].append(queue[0])

        # call parse_links function and input contents as parameter
        # return a list of links in one page
        links = parse_links(contents)

        # outgoing_links list
        outgoing_links = []

        # add links to the queue if not already looked at
        for l in links:
            full_link = get_full_url(l, seed)

            outgoing_links.append(full_link)

            if full_link in incoming_links:
                incoming_links[full_link].append(queue[0])
            else:
                incoming_links[full_link] = [queue[0]]

            if full_link not in links_visited:
                ID += 1
                links_visited[full_link] = ID
                map_ID_to_URL[ID] = full_link

                queue.append(full_link)

        # BEFORE REMOVING, ADD CONTENTS TO FILES
        global_functions.write_to_file(
            dirname, "outgoing_links.txt", outgoing_links)
        global_functions.write_to_file(dirname, "tf.txt", tf)

        # remove the first URL
        queue.pop(0)

    global_functions.write_to_file("data", "length.txt", len(links_visited))
    global_functions.write_to_file("data", "links_visited.txt", links_visited)
    # global_functions.write_to_file("data", "map_id_to_url.txt", map_ID_to_URL)

    write_incoming_links_to_files(incoming_links)
    write_idf_to_file(links_visited, word_appears)
    write_tfidf_to_files(links_visited)
    write_page_rank_to_files(seed, links_visited, map_ID_to_URL)

    return len(links_visited)
