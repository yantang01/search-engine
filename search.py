import math

import global_functions


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
    idfs = global_functions.read_file("data", "idf.txt")
    if word not in idfs:
        return 0
    return idfs[word]


def get_query_vector(query):
    vector = {}
    for word in query.split(" "):
        if word in vector:
            continue
        vector[word] = math.log(
            (1 + get_tf_query_word(query, word)), 2) * get_idf_query_word(word)
    return list(vector.values())


def get_page_vector(query, link):
    dirname = global_functions.get_dirname(link)
    tfidfs = global_functions.read_file(dirname, "tf-idfs.txt")
    vector = {}
    for word in query.split(" "):
        if word in vector:
            continue
        if word not in tfidfs:
            vector[word] = 0
            continue

        vector[word] = tfidfs[word]

    return list(vector.values())


def similarity(query, doc):
    numerator = 0
    left_denom = 0
    right_denom = 0
    for i in range(len(query)):
        numerator += (query[i] * doc[i])
        left_denom += (query[i] * query[i])
        right_denom += (doc[i] * doc[i])
    if numerator == 0:
        return 0
    similarity = numerator / (math.sqrt(left_denom) * math.sqrt(right_denom))
    return similarity


def search(query, boost):
    links_visited = global_functions.read_file("data", "links_visited.txt")

    top_list = []
    query_vector = get_query_vector(query)

    for link in links_visited:
        dirname = global_functions.get_dirname(link)
        entry = {}
        entry["url"] = link
        entry["title"] = global_functions.read_file(dirname, "title.txt")
        page_vector = get_page_vector(query, link)
        s = similarity(query_vector, page_vector)
        if boost == True:
            s = s * float(global_functions.read_file(dirname, "page_rank.txt"))
        entry["score"] = s
        top_list.append(entry)

    top_list = sorted(top_list, key=lambda i: i['score'], reverse=True)

    return top_list[0:10]
