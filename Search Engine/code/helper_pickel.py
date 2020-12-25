import pickle

posting_l = []


def read_pickle():
    with (open("posting_list.pickle", "rb")) as openfile:
        while True:
            try:
                posting_l.append(pickle.load(openfile))
            except EOFError:
                break
    print(len(posting_l[0]))


def main():
    read_pickle()


if __name__ == "__main__":
    main()
