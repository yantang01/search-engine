import searchdata
import math


def get_query_vector(query):
    vector = {}
    for word in query.split(" "):
        if word in vector:
            continue
        vector[word] = math.log(
            (1 + searchdata.get_tf_query_word(query, word)), 2) * searchdata.get_idf_query_word(word)
    return list(vector.values())


def get_page_vector(query, link):
    dirname = searchdata.get_dirname(link)
    tfidfs = searchdata.read_file(dirname, "tf-idfs.txt")
    vector = {}
    for word in query.split(" "):
        if word in vector:
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
    links_visited = searchdata.read_file("data", "links_visited.txt")

    top_list = []
    query_vector = get_query_vector(query)

    for link in links_visited:
        dirname = searchdata.get_dirname(link)
        entry = {}
        entry["url"] = link
        entry["title"] = searchdata.read_file(dirname, "title.txt")
        page_vector = get_page_vector(query, link)
        s = similarity(query_vector, page_vector)
        if boost == True:
            s = s * float(searchdata.read_file(dirname, "page_rank.txt"))
        entry["score"] = s
        top_list.append(entry)

    top_list = sorted(top_list, key=lambda i: i['score'], reverse=True)

    return top_list[0:10]
