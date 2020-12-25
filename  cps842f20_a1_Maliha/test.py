
import csv
from colorama import Style
from colorama import Back
import timeit
from invert import *


# Helper function to read the saved dictionary
def read_dictionary():
    dict = OrderedDict()

    with open('dictionary.csv') as csv_dict:

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


# Helper function to read the posting dictionary
def read_posting_list_file(dict, query_term):

    with open('posting_list.txt') as f:
        post_index = 0
        lines = f.readlines()
        for dict_key in dict.keys():
            if dict_key == query_term:
                break
            post_index = post_index + int(dict[dict_key]) * 2

    flag = post_index + int(dict[dict_key]) * 2
    return lines, post_index, flag


# Helper function find the document number for query term if it is presented
def find_doc_num(term):
    term_posting_list = find_position(',', term)
    return term[term_posting_list[len(term_posting_list)-1]+2:len(term)]


# Function to check the word if it is in the document
def check_word(word, doc):
    for elem in doc:
        if word in elem:
            return doc.index(elem)
    return -1


# Checking the document frequency + where in the documents the query term is found and
# how many times it appeared in the documents
# Also print the title
def check_document_frequency(query_term, dict):

    print("This query term is seen in " + dict[query_term] + " documents.")

    # Read posting list
    lines, post_index, posting_flag = read_posting_list_file(dict, query_term)

    while post_index < posting_flag:

        doc_num = str(int(find_doc_num(lines[post_index])) - 1)

        print('Document number ' + str(int(find_doc_num(lines[post_index]))) + " :")

        print('Given query term is seen in the document ' + lines[post_index][
                                                      0: find_position(',', lines[post_index])[0]] + ' times.')

        if doc_list[int(doc_num)].get('T') is not None and doc_list[int(doc_num)].get('W') is not None:

            title = doc_list[int(doc_num)].get('T')
            abstract = doc_list[int(doc_num)].get('W')
            print('Title: ')
            print(" ".join(str(num) for num in doc_list[int(doc_num)].get('T')) + "\n")

            if query_term in title or check_word(query_term, title) != -1:

                if query_term in title:
                    query_flag = title.index(query_term)
                else:
                    query_flag = check_word(query_term, title)

                if query_flag - 1 >= 0:
                    if query_flag - 6 >= 0:
                        statement_q = " ".join(str(point) for point in title[query_flag - 6:query_flag])
                    else:
                        statement_q = " ".join(str(point) for point in title[0:query_flag])
                else:
                    statement_q = ""

                if query_flag + 1 <= len(title):
                    if query_flag + 6 <= len(title):
                        statement_q2 = " ".join(str(x) for x in title[query_flag + 1:query_flag + 6])
                    else:
                        statement_q2 = " ".join(str(x) for x in title[query_flag + 1:len(title)])
                else:
                    statement_q2 = ""
                print(statement_q + " " + Back.CYAN + title[query_flag] + Style.RESET_ALL + " " + statement_q2)

            if query_term in abstract or check_word(query_term, abstract) != -1:
                if query_term in abstract:
                    query_flag = abstract.index(query_term)
                else:
                    query_flag = check_word(query_term, abstract)

                if query_flag - 1 >= 0:
                    if query_flag - 6 >= 0:
                        statement_q1 = " ".join(str(x) for x in abstract[query_flag - 6:query_flag])
                    else:
                        statement_q1 = " ".join(str(x) for x in abstract[0:query_flag])
                else:
                    statement_q1 = ""

                if query_flag + 1 <= len(abstract):
                    if query_flag + 6 <= len(abstract):
                        statement_q2 = " ".join(str(x) for x in abstract[query_flag + 1:query_flag + 6])
                    else:
                        statement_q2 = " ".join(str(x) for x in abstract[query_flag + 1:len(abstract)])
                else:
                    statement_q2 = ""
                print(statement_q1 + " " + Back.CYAN + abstract[query_flag] + Style.RESET_ALL + " " + statement_q2)

            if query_term in abstract or check_word(query_term, abstract) != -1:

                if query_term in abstract:
                    query_flag = abstract.index(query_term)
                else:
                    query_flag = check_word(query_term, abstract)

                if query_flag-1 >= 0:
                    if query_flag-6 >= 0:
                        statement_q1 = " ".join(str(x) for x in abstract[query_flag-6:query_flag])
                    else:
                        statement_q1 = " ".join(str(x) for x in abstract[0:query_flag])
                else:
                    statement_q1 = ""

                if query_flag + 1 <= len(abstract):
                    if query_flag + 6 <= len(title):
                        statement_q2 = " ".join(str(x) for x in abstract[query_flag+1:query_flag + 6])
                    else:
                        statement_q2 = " ".join(str(x) for x in abstract[query_flag+1:len(abstract)])
                else:
                    statement_q1 = ""

                print(statement_q1 + " " + Back.CYAN + abstract[query_flag] + Style.RESET_ALL + " " + statement_q2)

        elif doc_list[int(doc_num)].get('T') is not None and doc_list[int(doc_num)].get('W') is None:

            title = doc_list[int(doc_num)].get('T')
            print('Title : ')
            print(" ".join(str(x) for x in doc_list[int(doc_num)].get('T')) + "\n")

            if query_term in title:
                query_flag = title.index(query_term)
            else:
                query_flag = check_word(query_term, title)
            if query_flag - 1 >= 0:
                if query_flag - 6 >= 0:
                    statement_q1 = " ".join(str(x) for x in title[query_flag - 6:query_flag])
                else:
                    statement_q1 = " ".join(str(x) for x in title[0:query_flag])
            else:
                statement_q1 = ""

            if query_flag + 1 <= len(title):
                if query_flag + 6 <= len(title):
                    statement_q2 = " ".join(str(x) for x in title[query_flag + 1:query_flag + 6])
                else:
                    statement_q2 = " ".join(str(x) for x in title[query_flag + 1:len(title)])
            else:
                statement_q2 = ""
            print(statement_q1 + " " + Back.CYAN + title[query_flag] + Style.RESET_ALL + " " + statement_q2)

        else:
            abstract = doc_list[int(doc_num)].get('W')

            if query_term in abstract:
                query_flag = doc_list.index(query_term)
            else:
                query_flag = check_word(query_term, abstract)

            if query_flag - 1 >= 0:
                if query_flag - 6 >= 0:
                    statement_q1 = " ".join(str(x) for x in abstract[query_flag - 6:query_flag])
                else:
                    statement_q1 = " ".join(str(x) for x in abstract[0:query_flag])
            else:
                statement_q1 = ""

            if query_flag + 1 <= len(abstract):
                if query_flag + 6 <= len(abstract):
                    statement_q2 = " ".join(str(x) for x in abstract[query_flag + 1:query_flag + 6])
                else:
                    statement_q2 = " ".join(str(x) for x in abstract[query_flag + 1:len(abstract)])
            else:
                statement_q2 = ""

            print(statement_q1 + " " + Back.CYAN + abstract[query_flag] + Style.RESET_ALL + " " + statement_q2)

        print('positions : ' + lines[post_index][
                               find_position(',', lines[post_index])[0] + 1:find_position(',', lines[post_index])[
                                   len(find_position(',', lines[post_index])) - 2]])
        print('-------------------------------------------\n')
        post_index = post_index + 2


# Main test function where all the helper functions are being called
# User first takes a query terms as input and then search for it in the saved dictionary
def test():

    print('Testing Started....')
    total_time = 0

    dict = read_dictionary()

    print('Dictionary read done from csv file!')

    # The user will keep inputting a query term unless the user types in "ZZEND"
    while True:
        query_term = input('Please enter a word as Query: ')

        # It calculates the processing time by setting a timer
        start = timeit.default_timer()
        if query_term == 'ZZEND':
            break

        if query_term not in dict:
            print('The query term does not exist in the dictionary!!')

        else:

            check_document_frequency(query_term, dict)
            stop = timeit.default_timer()
            process_time = stop - start
            total_time += process_time
            print('Total time spent to search this query term: ', process_time)


# The main function which will first call the invert function to create the dictionary and posting list
# Then call the test function to check with any query term
if __name__ == '__main__':
    main()
    test()
