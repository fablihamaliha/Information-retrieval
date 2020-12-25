import numpy as np
import re
import nltk
import string
import collections
import cleaning
import math
import pickle
N_pages = 10000  # num of pages to be inversted and parsed # you can get from the num of folders in file


def create_dict_posting(bag):
    m_dict = collections.OrderedDict()
    posting = list()
    i = 0
    for tup in bag:
        word = tup[0]
        doc_id = tup[1]
        if word in m_dict.keys():
            val = m_dict[word]
            post_val = posting[val[1]]
            if doc_id in post_val.keys():
                posting[val[1]][doc_id] += 1
            else:
                m_dict[word][0] += 1
                posting[val[1]].update({doc_id: 1})

        else:
            m_dict[word] = [1, i]  # doc frequency
            posting.append({doc_id: 1})  # term frequency
            i += 1

    return m_dict, posting


def create_bag_words(doc_body_list):
    bag = list()
    for doc in doc_body_list:
        for word in doc[1]:
            bag.append((word, doc[0]))
    s_bag = sorted(bag, key=lambda x: x[0])
    return s_bag


def create_length_dict(m_dict, potsing, N):
    d_dict = dict()
    for word in m_dict.keys():
        val_dict = m_dict[word]
        idf = math.log10(N/val_dict[0])
        post_ind = val_dict[1]
        docs = potsing[post_ind]
        for doc in docs.keys():
            if doc in d_dict.keys():
                f = docs[doc]
                tf = 1+math.log10(f)
                wij = tf+idf
                d_dict[doc] += math.pow(wij, 2)

            else:
                f = docs[doc]
                tf = 1+math.log10(f)
                wij = tf+idf
                d_dict[doc] = math.pow(wij, 2)
    return d_dict  # need to get sqrt of each elemn when using

# call the clean object on all and create the dict and posting list and length dictionary


def run_invert():
    m_dict = collections.OrderedDict()
    d_dict = dict()
    posting = list()
    doc_body_list = list()
    website = "Ryerson"
    for docID in range(N_pages):

        parser = cleaning.Parser()
        parser.read_stop_words("common_words")
        parser.read_doc(website, docID)
        parser.clean_html()
        parser.my_tokenize()
        doc_body = [docID, parser.get_tokens()]
        doc_body_list.append(doc_body)
    parser2 = cleaning.Parser()
    web_graph = parser2.preprocess_documents()
    bag = create_bag_words(doc_body_list)
    m_dict, posting = create_dict_posting(bag)
    d_dict = create_length_dict(m_dict, posting, N_pages)

    with open('Dictionary.pickle', 'wb') as handle:
        pickle.dump(m_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('posting_list.pickle', 'wb') as handle:
        pickle.dump(posting, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('web_graph.pickle', 'wb') as handle:
        pickle.dump(web_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('doc_length_dict.pickle', 'wb') as handle:
        pickle.dump(d_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # return m_dict, posting, N_pages


def main():
    run_invert()


if __name__ == "__main__":
    main()
