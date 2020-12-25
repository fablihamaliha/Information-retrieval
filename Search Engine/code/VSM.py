import math
import m_invert
import UI
import cleaning
import pickle
import helper_pickel
N = 10000  # fix this


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


def find_docs(q_tokens, m_dict, posting):
    list_docs = list()
    for word in q_tokens:
        if word in m_dict.keys():
            post_ind = m_dict[word][1]
            doc_IDs = posting[post_ind].keys()
            list_docs.extend(list(doc_IDs))
    return set(list_docs)  # just added


def create_q_weight(q):  # did not put idf for query
    q2 = list(set(q))
    wq = [0]*len(q2)
    i = 0
    for q_word in q2:
        f = q.count(q_word)
        tf = 1+math.log10(f)
        wq[i] = tf
        i += 1
    return wq


def cosi_sim(wq, list_docs, query_tokens, m_dict, posting, d_dict, N):
    q_tokens = list(set(query_tokens))
    sim_list = list()

    tmp_q = [math.pow(x, 2) for x in wq]
    q_d = math.sqrt(sum(tmp_q))
    for doc in list_docs:
        sum_w = 0
        i = -1
        for word in q_tokens:
            i += 1
            if word in m_dict:
                val_dict = m_dict[word]
                df = val_dict[0]
                post_ind = val_dict[1]
                val_post = posting[post_ind]
                if doc in val_post.keys():
                    idf = math.log10(N/df)
                    f = val_post[doc]
                    tf = 1+math.log10(f)
                    wij = tf*idf
                    wq_wij = wij*wq[i]
                    sum_w += wq_wij
        d_d = math.sqrt(d_dict[doc])
        score = sum_w/(d_d*q_d)
        sim_list.append((doc, round(score, 5)))

    return sim_list


def run_VSM(q_tokens, Num_of_Results):

    m_dict = dict()
    posting = list()
    d_dict = dict()

    # with open('url_from_code_dict.pickle', 'rb') as handle:
    #     url_from_code = pickle.load(handle)
    with open('doc_length_dict.pickle', 'rb') as handle:
        d_dict = pickle.load(handle)
    with open('Dictionary.pickle', 'rb') as handle:
        m_dict = pickle.load(handle)
    with open("posting_list.pickle", 'rb') as handle:
        posting = pickle.load(handle)
    with open("page_rank.pickle", 'rb') as handle:
        pg = pickle.load(handle)

    # query = UI.ask_query()
    # p = cleaning.Parser()
    # q_tokens = p.tokenize_query(query)
    wq = create_q_weight(q_tokens)
    docs = find_docs(q_tokens, m_dict, posting)
    sim_score = cosi_sim(wq, docs, q_tokens, m_dict, posting, d_dict, N)
    doc_score = sorted(sim_score, key=lambda tup: tup[1], reverse=True)
    end = min(len(doc_score), Num_of_Results)
    doc_score2 = doc_score[0:end]

    # docs = [e[0] for e in doc_score2]
    # pg_scores = [pg[e] for e in docs]
    # new_score_docs = list()
    # for i in range(len(docs)):

    #     hyb_score = pg_scores[i]*0.7+doc_score2[i][1]*0.3
    #     tmp = (docs[i], hyb_score)
    #     new_score_docs.append(tmp)

    # doc_score_new = sorted(
    #     new_score_docs, key=lambda tup: tup[1], reverse=True)
    # docs_new = [e[0] for e in doc_score_new]
    # docs_new2 = docs_new[0:end]
    # UI.display_query_results(docs_new2, url_from_code, q_tokens)

    # for now only 100 pages
    # return doc_score2[0:end]
    return doc_score2
