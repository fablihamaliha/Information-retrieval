import collections
from nltk.stem import PorterStemmer
from search import TFIDF
# from search import IDF
from search import cosine_similarity
import operator
from eval import *
import csv
from invert import *


def arrange_words(input_list, w_index, isstemm):
    sentence = ""
    ps = PorterStemmer()

    while input_list[w_index] != ".N\n":
        if input_list[w_index] == ".A\n":
            break

        sentence = sentence + ps.stem(input_list[w_index]) if isstemm == 1 else sentence + input_list[w_index]

        sentence = sentence + " "
        w_index = w_index + 1

    return sentence


def read_query_file(isstemm):

    doc_list = []

    # oen the query.txt file
    q_file = open("cacm/query.text", "r")
    q_lines = q_file.readlines()

    for i in range(len(q_lines)):

        if q_lines[i] == ".W\n":
            doc_list.append(arrange_words(q_lines, i+1, isstemm))

    return doc_list


def read_qrels_file():

    doc_list = []

    # oen the qrels.txt file
    q_file = open("cacm/qrels.text", "r")
    q_lines = q_file.readlines()

    length_qrels = int(word_tokenize(q_lines[len(q_lines)-1])[0])

    print('Size of the Qrels file: ', length_qrels)

    # Creating a dummy list
    for i in range(length_qrels):
        temp = []
        doc_list.append(temp)

    for l in range(len(q_lines)):

        item = word_tokenize(q_lines[l])
        item_list = doc_list[int(item[0])-1]
        item_list.append(item[1])
        doc_list[int(item[0])-1] = item_list

    return doc_list


def read_dictionary():
    dict = OrderedDict()

    with open('dict.csv') as csv_dict:

        csv_dict_reader = csv.reader(csv_dict, delimiter=',')
        for line in csv_dict_reader:

            if len(line) == 2:
                dict.update({line[0]: line[1]})
            else:
                word = ''
                for i in range(len(line) - 1):
                    word = word + line[i] + ","

                word = word[0:len(word) - 1]
                dict.update({word: line[len(line) - 1]})
    return dict


def remove_stop_words_from_query(query, stop_words_list, isstemmed):
    ps = PorterStemmer()
    word_tokens = word_tokenize(query)
    
    filtered_query = []
    
    for w in word_tokens: 
        if w not in stop_words_list:

            filtered_query.append(ps.stem(w)) if isstemmed == 'y' else filtered_query.append(w) 

    return filtered_query


def find_query_position(query, doc):

    pos_list = []
    query_index = doc.find(query)
    total = 0

    while query_index != -1:
        total = total + query_index
        pos_list.append(total)
        total = total + len(query)
        doc = doc[query_index + len(query): len(doc)]
        query_index = doc.find(query)

    return pos_list


def find_query(query):
    pos_list = find_query_position(',', query)
    return query[pos_list[len(pos_list)-1]+2:len(query)]


def search_query(query, isstemmed, dict):
    query_words = remove_stop_words_from_query(query.lower(), stop_words_list, isstemmed)
    # print(query_words)
    
    list_mul = collections.OrderedDict()
    post_list = []
    
    visited = []
    
    for i in range(len(query_words)):
        if query_words[i] in visited:
            break
        else:
            visited.append(query_words[i])

        query = query_words[i]

        if query in dict:
            # print(query)

            temp_doc_list = []

            with open('posting_list.txt') as f:
                posting_index = 0
                f_line = f.readlines()
                for key in dict.keys():
                    if key == query:
                        break
                    posting_index = posting_index + int(dict[key]) * 2

            posting_flag = posting_index + int(dict[key]) * 2

            while posting_index < posting_flag:
                doc_number = str(int(find_query(f_line[posting_index])) - 1)
                if doc_number not in temp_doc_list:
                    temp_doc_list.append(doc_number)
                posting_index = posting_index + 2

            temp_score = {}

            # count = len(temp_doc_list)
            #
            # if len(temp_doc_list) > 15:
            #     count = 15

            for j in range(len(temp_doc_list)):
                body = []

                if doc_list[int(temp_doc_list[j])].get('T') is not None and \
                        doc_list[int(temp_doc_list[j])].get('W') is not None:

                    body = doc_list[int(temp_doc_list[j])].get('T') + \
                           doc_list[int(temp_doc_list[j])].get('W')

                    if doc_list[int(temp_doc_list[j])].get('A') is not None:
                        body = body + doc_list[int(temp_doc_list[j])].get('A')

                if doc_list[int(temp_doc_list[j])].get('T') is not None and \
                        doc_list[int(temp_doc_list[j])].get('W') is None:

                    body = doc_list[int(temp_doc_list[j])].get('T')

                    if doc_list[int(temp_doc_list[j])].get('A') is not None:
                        body = body + doc_list[int(temp_doc_list[j])].get('A')

                else:
                    body = doc_list[int(temp_doc_list[j])].get('W')

                    if doc_list[int(temp_doc_list[j])].get('A') is not None:
                        body = body + doc_list[int(temp_doc_list[j])].get('A')

                v1, v2 = TFIDF(dict, body, query_words, len(doc_list))

                similarity = cosine_similarity(v1, v2)
                temp_score.update({temp_doc_list[j]: similarity})

            sorted_score = sorted(temp_score.items(), key=operator.itemgetter(1))

            if len(sorted_score) < 30:

                for q in range(0, len(sorted_score)):
                    ind, sc = sorted_score[len(sorted_score) - 1 - q]
                    list_mul.update({ind: sc})
            else:
                for q in range(0, 30):
                    ind, sc = sorted_score[len(sorted_score) - 1 - q]
                    list_mul.update({ind: sc})

    score = collections.OrderedDict()
    sorted_score = sorted(list_mul.items(), key=operator.itemgetter(1))

    if len(sorted_score) < 30:
        for q in range(0, len(sorted_score)):
            ind, sc = sorted_score[len(sorted_score) - 1 - q]
            score.update({ind: sc})
    else:
        for q in range(0, 30):
            ind, sc = sorted_score[len(sorted_score) - 1 - q]
            score.update({ind: sc})

    score = sorted(score.items(), key=operator.itemgetter(1))

    for i in range(len(score)):
        print('----------------------------------------')
        print("Rank: ", i + 1)
        id_doc = doc_list[int(ind)].get('I')

        ind, sc = score[len(score) - 1 - i]
        print("Document ID:", int(ind)+1)
        post_list.append(id_doc)

        print('Title: ', doc_list[int(ind)].get('OT'))

        if doc_list[int(ind)].get('A') is not None:
            print('Author(s): ', doc_list[int(ind)].get('OA'))

        print("Score: " + str(sc))
        print('--------------------------------------------')

    return post_list


def test():

    # Take input from user
    stem_input_user = input("stemming Query.txt file? Y/N: ")

    print('Reading queries and qrels file!')
    queries = read_query_file(stem_input_user)
    qrels = read_qrels_file()

    dict = read_dictionary()
    print('Dictionary read done from csv file!')

    # Part 3: Checking the search function with user query

    query_term = input('Please enter a phrase as Query: ')

    isstemmed = input("Do you want your query to be stemmed(y/n): ")
    
    if isstemmed == 'y':
         ps = PorterStemmer()
         query_term = ps.stem(query_term)

    list_queries = search_query(query_term, isstemmed, dict)
    print('List of documents where the query term occurs:', list_queries)

    # Part 4: Started Evaluation
    print('Started Evaluation!')

    mean_average_prcision = []
    mean_r_precision = []

    for i in range(0, len(queries)):
        search_res = search_query(queries[i], isstemmed, dict)

        if len(search_res) == 0 or len(qrels[i]) == 0:
            print("O search results or 0 qrels elements found! Skipping precision calculation!")
            continue

        # Calculate recall and precision
        ap_value = get_average_precision(search_res, qrels[i])
        mean_average_prcision.append(ap_value)
        print('Average precision value(%) for query ' + str(i) + ': ', ap_value)

        r_precision_value = get_r_precision(search_res, qrels[i])
        mean_r_precision.append(r_precision_value)
        print('R precision value(%) for query ' + str(i) + ': ', r_precision_value)

    print("-------------------------------------------")
    print("Calculating average values for the queries!")
    print("-------------------------------------------")
    print('Average MAP: ', sum(mean_average_prcision)/len(mean_average_prcision))
    print('Average R-Precision: ', sum(mean_r_precision) / len(mean_r_precision))


# The main function which will first call the invert function to create the dictionary and posting list
# Then call the test function to check with any query term
if __name__ == '__main__':
    print("Invert process started! generating dictionary and positing file")
    main()

    print("Searching started! ")
    test()
