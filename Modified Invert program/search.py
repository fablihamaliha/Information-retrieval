import numpy as np
import math
from collections import Counter


# Calculate TF
def TF(input_dict, doc, query):

    vec1 = np.zeros(len(doc) + len(query))
    vec2 = np.zeros(len(doc) + len(query))

    occ1 = Counter(doc)
    occ2 = Counter(query)

    dic = {}

    for i in range(len(doc)):
        if doc[i] not in dic:
            dic.update({doc[i]: i})

    for i in range(len(query)):
        if query[i] not in dic:
            dic.update({query[i]: i + len(doc)})

    for i in range(len(doc)):
        if doc[i] in input_dict.keys():
            temp = 1 + math.log(occ1.get(doc[i]), 10)
            vec1[dic.get(doc[i])] = temp

    for i in range(len(query)):
        if query[i] in input_dict.keys():
            temp = 1 + math.log(occ2.get(query[i]), 10)
            vec2[dic.get(query[i])] = temp

    return vec1, vec2


# Calculate IDF query
def IDF(input_dict, number, doc, query):
    vector = np.zeros(len(doc) + len(query))
    dic = {}

    for i in range(len(doc)):
        if doc[i] not in dic:
            dic.update({doc[i]:i})

    for i in range(len(query)):
        if query[i] not in dic:
            dic.update({query[i]:i+len(doc)})

    for key, value in dic.items():
        if key in input_dict.keys():
            v2 = input_dict.get(key)
            vector[value] = math.log(1 + (number/int(v2)), 10)

    return vector


# Calculate the TFIDF
def TFIDF(input_dict, doc, query, length):

    tf_doc, tf_query = TF(input_dict, doc, query)
    idf = IDF(input_dict, length, doc, query)
    doc, query = tf_doc * idf, tf_query * idf

    return doc, query


# measure the cosine similarity between two
def cosine_similarity(vec1, vec2):
    inner_prod = np.inner(vec1, vec2)
    norm_vec1, norm_vec2 = np.linalg.norm(vec1), np.linalg.norm(vec2)

    return inner_prod/(norm_vec1 * norm_vec2)
