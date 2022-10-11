import searchdata
import math


def get_query_vector(query):
    # 1. Get query vector
    vector = {}
    for word in query.split(" "):
        if word in vector:
            continue
        vector[word] = math.log(
            (1 + searchdata.get_tf_query_word(query, word)), 2) * searchdata.get_idf_query_word(word)
    return vector


vector = {'apple': 0.5102439583250715, 'peach': 0.5145731728297582}
vector = list(vector.values())
print(vector)