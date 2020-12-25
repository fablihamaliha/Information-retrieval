import page_rank
import pickle

MAX_ITERATION = 200


def main():

    with open('web_graph.pickle', 'rb') as handle:
        web_g = pickle.load(handle)

    print('Running page rank')
    p_ranker = page_rank.PageRank()
    page_ranks = p_ranker.page_rank(web_g, MAX_ITERATION)
    with open('page_rank.pickle', 'wb') as handle:
        pickle.dump(page_ranks, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
