import os
import global_functions


def get_outgoing_links(URL):
    dirname = global_functions.get_dirname(URL)
    if not os.path.isdir(dirname):
        return None
    outgoing_links = global_functions.read_file(dirname, "outgoing_links.txt")
    return outgoing_links


def get_incoming_links(URL):
    dirname = global_functions.get_dirname(URL)
    if not os.path.isdir(dirname):
        return None
    incoming_links = global_functions.read_file(dirname, "incoming_links.txt")
    return incoming_links


def get_page_rank(URL):
    dirname = global_functions.get_dirname(URL)

    if not os.path.isdir(dirname):
        return -1

    return global_functions.read_file(dirname, "page_rank.txt")


# term frequency
def get_tf(URL, word):
    dirname = global_functions.get_dirname(URL)

    if not os.path.isdir(dirname):
        return 0

    tf = global_functions.read_file(dirname, "tf.txt")

    if word not in tf:
        return 0

    return tf[word]


# IDFs
def get_idf(word):
    idf = global_functions.read_file("data", "idf.txt")

    if word not in idf:
        return 0

    return idf[word]


# tf-idfs
def get_tf_idf(URL, word):
    dirname = global_functions.get_dirname(URL)

    if not os.path.isdir(dirname):
        return 0

    tfidf = global_functions.read_file(dirname, "tf-idfs.txt")

    if word not in tfidf:
        return 0

    return tfidf[word]
