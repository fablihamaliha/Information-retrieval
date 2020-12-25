import VSM
import UI
import pickle
import collections
import cleaning
import webbrowser


# url_from_code_dict ==> ID:link to show result


def open_website(url):
    webbrowser.open(url.split()[0], new=2, autoraise=True)


def read_pick_files(file_name):
    inf = open(file_name, 'rb')
    new_dict = pickle.load(inf)
    inf.close()
    return new_dict


def handle_show_query(best_ranked, query_tokens, url_from_code):
    choice = UI.display_query_results(
        best_ranked, url_from_code, query_tokens)

    if choice is None:
        return False

    else:
        if choice == 'search':
            choice = UI.display_query_results(
                best_ranked, url_from_code, query_tokens)
        else:
            open_website(choice)


def main():
    w1 = 0.3
    w2 = 1-w1
    new_score_docs = list()
    url_from_code = read_pick_files("url_from_code_dict.pickle")
    pg = read_pick_files("page_rank.pickle")
    # query = UI.ask_query()
    # p = cleaning.Parser()
    # q_tokens = p.tokenize_query(query)
    # # fix: change the number of relavant resulats
    # vsm_docs_score = VSM.run_VSM(q_tokens, 100)
    # docs = [e[0] for e in vsm_docs_score]
    # pg_scores = [pg[e] for e in docs]
    # for i in range(len(docs)):
    #     hyb_score = pg_scores[i]*w1+vsm_docs_score[i][1]*w2
    #     tmp = (docs[i], hyb_score)
    #     new_score_docs.append(tmp)

    # doc_score_new = sorted(
    #     new_score_docs, key=lambda tup: tup[1], reverse=True)
    # docs_new = [e[0] for e in doc_score_new]
    # handle_show_query(docs_new, q_tokens, url_from_code)
    # #UI.display_query_results(docs_new, url_from_code, q_tokens)
    while(True):
        new_score_docs = list()
        query = UI.ask_query()
        if query == None:
            exit()
        p = cleaning.Parser()
        q_tokens = p.tokenize_query(query)

        vsm_docs_score = VSM.run_VSM(q_tokens, 100)
        docs = [e[0] for e in vsm_docs_score]

        if docs == []:
            UI.handle_show_no_resualts()
            continue
        pg_scores = [pg[e] for e in docs]
        for i in range(len(docs)):
            hyb_score = pg_scores[i]*w1+vsm_docs_score[i][1]*w2
            tmp = (docs[i], hyb_score)
            new_score_docs.append(tmp)

        doc_score_new = sorted(
            new_score_docs, key=lambda tup: tup[1], reverse=True)
        docs_new = [e[0] for e in doc_score_new]

        e = handle_show_query(docs_new, q_tokens, url_from_code)
        if e == False:
            exit()


if __name__ == "__main__":
    main()
