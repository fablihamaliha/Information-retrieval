
from nltk.tokenize import word_tokenize
import nltk
from collections import OrderedDict
nltk.download('punkt')


# Helper Functions

# Creating the posting class with position, term frequency and the document ID
class Posting:
    def __init__(self, pos, term_freq, document_id):
        self.positions = pos
        self.TD = term_freq
        self.ID = document_id


# Reading the given cacam files
def read_cacm_file():
    cacm_reader = open('cacm/cacm.all', 'r')
    cacm_lines = cacm_reader.readlines()

    return cacm_lines


# Reading the stop words  from given files
def read_stop_words_file():
    stop_words_reader = open('stopwords.txt', 'r')
    stop_words_list = set()
    stop_words = stop_words_reader.readlines()

    for _, word in enumerate(stop_words):
        stop_words_list.add(word.split('\n')[0])

    return stop_words_list


# Function for generating tokens
def generate_tokens(sentence):
    # return word_tokenize(string.lower())
    # tokens = sentence.split(' ')
    return word_tokenize(sentence.lower())


# Function for removing stop words
def remove_stop_words(sentence, stop_words_list):
    token_list = generate_tokens(sentence)
    processed_sentence = []

    for token in token_list:
        if token not in stop_words_list:
            processed_sentence.append(token)

    return processed_sentence


# Function for applying stemmer
def generate_stemmer(word_list):
    nltk_ps = nltk.PorterStemmer()

    if type(word_list) == 'str':
       word_list = generate_tokens(word_list)

    output_word_list = []
    for i, word in enumerate(word_list):
        output_word_list.append(nltk_ps.stem(word))
    return output_word_list


# Function for arranging words
def arrange_words(words_list, idx):
    arranged_words = ""

    while '.B' not in words_list[idx]:
        arranged_words = arranged_words + words_list[idx] + " "
        idx += 1
    return arranged_words


# Function for arranging authors
def arrange_authors(words_list, idx):
    arranged_authors = ""

    while words_list[idx] != ".N\n":
        if words_list[idx] == ".K\n" or words_list[idx] == ".C\n":
            break
        arranged_authors = arranged_authors + words_list[idx] + " "
        idx = idx + 1
    return arranged_authors


# Function for finding the positions from a list of words
def find_position(sentence, words_list):
    word_position_list = []
    temp_position_list = words_list
    idx_pos = 0
    if sentence in words_list:
        idx_pos = words_list.index(sentence, idx_pos)
        word_position_list.append(idx_pos)
        temp_position_list = words_list[idx_pos + 1: len(words_list)]
        while sentence in temp_position_list:
            idx_pos += 1
            idx_pos = words_list.index(sentence, idx_pos)
            word_position_list.append(idx_pos)
            temp_position_list = words_list[idx_pos+1:len(words_list)]
    return word_position_list

# Following are the global lists and record dictionary
#################################################
doc_list = []
record_dict = dict.fromkeys(['I', 'T', 'W', 'B', 'A'])
unique_word_index_list = []
postings_lists = []
doc_dict = OrderedDict()
##################################################


# Process the cacm data based on different keys
def process_cacm_data(cacm_lines, stop_input_user, stem_input_user, stop_words):

    for i in range(len(cacm_lines)):

        line = cacm_lines[i]

        if ".I " in line:
            record_dict = dict.fromkeys(['I', 'T', 'W', 'B', 'A'])
            record_dict['I'] = cacm_lines[i][2:len(cacm_lines)]

        if ".T" in line:

            if stop_input_user == 'n' and stem_input_user == 'n':
                record_dict['T'] = generate_tokens(cacm_lines[i+1].lower())

            elif stop_input_user == 'y' and stem_input_user == 'n':
                record_dict['T'] = remove_stop_words(cacm_lines[i + 1].lower(), stop_words)

            elif stop_input_user == 'n' and stem_input_user == 'y':
                token_gen = generate_tokens(cacm_lines[i + 1].lower())
                record_dict['T'] = generate_stemmer(token_gen)

            else:
                stop_word_removal = remove_stop_words(cacm_lines[i + 1], stop_words)
                record_dict['T'] = generate_stemmer(stop_word_removal)

        if ".W" in line:

            if stop_input_user == 'n' and stem_input_user == 'n':
                word_arr = arrange_words(cacm_lines, i + 1)
                record_dict['W'] = generate_tokens(word_arr)

            elif stop_input_user == 'y' and stem_input_user == 'n':
                word_arr = arrange_words(cacm_lines, i + 1)
                record_dict['W'] = remove_stop_words(word_arr, stop_words)

            elif stop_input_user == 'n' and stem_input_user == 'y':
                word_arr = arrange_words(cacm_lines, i + 1)
                token_gen = generate_tokens(word_arr)
                record_dict['W'] = generate_stemmer(token_gen)

            else:
                word_arr = arrange_words(cacm_lines, i+1)
                stop_word_removal = remove_stop_words(word_arr, stop_words)
                record_dict['W'] = generate_stemmer(stop_word_removal)

        if ".B" in line:
            record_dict['B'] = cacm_lines[i+1].split('\n')[0]

        if ".A" in line:
            author_list = generate_tokens(arrange_authors(cacm_lines, i+1))

            while '.' in author_list:
                author_list.remove('.')
            while ',' in author_list:
                author_list.remove(',')

            if stem_input_user == 'y':
                record_dict['A'] = generate_stemmer(author_list)

            else:
                record_dict['A'] = author_list

        if ".X" in line:
            doc_list.append(record_dict)


# Function for creating word index list based on the doct list from dictionary
def create_unique_word_index_list():
    for idx in range(len(doc_list)):

        title_list = doc_list[idx].get('T')
        abstract_list = doc_list[idx].get('W')
        authors_list = doc_list[idx].get('A')

        if title_list is not None:
            for t in range(len(title_list)):

                if title_list[t] not in unique_word_index_list:
                    unique_word_index_list.append(title_list[t])

        if abstract_list is not None:
            for abs in range(len(abstract_list)):

                if abstract_list[abs] not in unique_word_index_list:
                    unique_word_index_list.append(abstract_list[abs])

        if authors_list is not None:
            for aut in range(len(authors_list)):

                if authors_list[aut] not in unique_word_index_list:
                    unique_word_index_list.append(authors_list[aut])

    unique_word_index_list.sort()


# Function for creating thje posting list associated with word index
def create_postings_list():

    # Create an empty posting list
    for loop in range(len(unique_word_index_list)):
        individual_posting_list = []
        postings_lists.append(individual_posting_list)

    for doc in range(len(doc_list)):

        if doc_list[doc].get('T') is not None and doc_list[doc].get('W') is not None:
            combine_cat = doc_list[doc].get('T')
            combine_cat.extend(doc_list[doc].get('W'))

            if doc_list[doc].get('A') is not None:
               combine_cat.extend(doc_list[doc].get('A'))

        elif doc_list[doc].get('T') is not None and doc_list[doc].get('W') is None:
            combine_cat = doc_list[doc].get('T')

            if doc_list[doc].get('A') is not None:
                combine_cat.extend(doc_list[doc].get('A'))

        elif doc_list[doc].get('W') is not None:
            combine_cat = doc_list[doc].get('W')

            if doc_list[doc].get('A') is not None:
                combine_cat.extend(doc_list[doc].get('A'))

        else:
            continue

        store_posting = []

        # Checking the documents for Abstract
        if doc_list[doc].get('W') is not None:
            for abstract in range(len(doc_list[doc].get('W'))):
                if doc_list[doc].get('W')[abstract] not in store_posting:
                    individual_posting_list = postings_lists[unique_word_index_list.index(doc_list[doc].get('W')[abstract])]

                    t_position = find_position(doc_list[doc].get('W')[abstract], combine_cat)
                    store_posting.append(doc_list[doc].get('W')[abstract])
                    if len(t_position) != 0:
                        individual_posting_list.append(Posting(t_position, len(t_position), doc_list[doc].get('I')))
                        postings_lists[unique_word_index_list.index(doc_list[doc].get('W')[abstract])] = individual_posting_list

        # Checking the documents for Title
        if doc_list[doc].get('T') is not None:

            for title in range(len(doc_list[doc].get('T'))):
                if doc_list[doc].get('T')[title] not in store_posting:
                    individual_posting_list = postings_lists[unique_word_index_list.index(doc_list[doc].get('T')[title])]

                    t_position = find_position(doc_list[doc].get('T')[title], combine_cat)
                    if len(t_position) != 0:
                        individual_posting_list.append(Posting(t_position, len(t_position), doc_list[doc].get('I')))
                        postings_lists[unique_word_index_list.index(doc_list[doc].get('T')[title])] = individual_posting_list

        # Checking the documents for Authors
        if doc_list[doc].get('A') is not None:
            for author in range(len(doc_list[doc].get('A'))):
                if doc_list[doc].get('A')[author] not in store_posting:
                    individual_posting_list = postings_lists[unique_word_index_list.index(doc_list[doc].get('A')[author])]

                    t_position = find_position(doc_list[doc].get('A')[author], combine_cat)

                    if len(t_position) != 0:
                        individual_posting_list.append(Posting(t_position, len(t_position), doc_list[doc].get('I')))
                        postings_lists[unique_word_index_list.index(doc_list[doc].get('A')[author])] = individual_posting_list


# Function for creating the document dictionary which will update the dict with words
def create_document_dict():
    for word in range(len(unique_word_index_list)):
        doc_dict.update({unique_word_index_list[word]: len(postings_lists[word])})


# Function for saving dictinary output to file and creating dictionary.csv
def save_dict_output_to_file():
    with open('dictionary.csv', 'w') as file:
        for doc_key in doc_dict.keys():

            file.write("%s,%s\n" % ('","', doc_dict[doc_key])) if doc_key == ',' else \
                file.write("%s,%s\n" % (doc_key, doc_dict[doc_key]))
    file.close()


# Function for creating the posting_list.txt
def create_file_posting_list():
    with open('posting_list.txt', 'w') as f:
        for post in range(len(postings_lists)):
            t_post = postings_lists[post]
            for one_post in range(len(postings_lists[post])):
                f.write("%s" % (len(t_post[one_post].positions)))
                f.write(",")
                for position in range(len(t_post[one_post].positions)):
                    f.write("%s" % (t_post[one_post].positions[position]))
                    f.write(",")
                f.write("%s" % (t_post[one_post].TD))
                f.write(",")
                f.write("%s" % (t_post[one_post].ID))
                f.write("-------------------------------------------\n")
    f.close()


# Main function which will call all the helper functions
def main():

    # read cacm and common words file
    cacm_lines = read_cacm_file()
    stop_words = read_stop_words_file()

    # Take input from user
    stop_input_user = input("Want to STOP word removal?? Please Type Y/N: ")
    stem_input_user = input("stemming? Y/N: ")

    # Process cacm data based on common words
    process_cacm_data(cacm_lines, stop_input_user, stem_input_user, stop_words)
    print('Data processing Done!!!')

    # Create the posting file
    create_unique_word_index_list()
    print(len(unique_word_index_list))

    create_postings_list()
    print('Posting creation Done!!!')

    # Create the dictionary
    create_document_dict()
    print('Document Dict creation Done!!!')

    # Saving the words in file as csv
    save_dict_output_to_file()
    create_file_posting_list()
    print('Save output to file Done!!!')


if __name__ == '__main__':
    main()


        
            
    

    
            
            


            

