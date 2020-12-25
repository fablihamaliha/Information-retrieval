from selectolax.parser import HTMLParser
import re
import string
import nltk
import pickle
from link_extractor import LinkExtractor
from domain_utils import *
import graph
import page_rank
STOP_WORDS = set()
ps = nltk.PorterStemmer()


class Parser:
    def __init__(self, n_pages=10000):
        self.clean_raw = ''
        self.tokens = []
        self.raw_body = ''
        self.n_pages = n_pages
        self.FOLDER = 'Ryerson'
        self.HOMEPAGE = 'https://www.ryerson.ca/'
        self.DOMAIN_NAME = get_domain_name(self.HOMEPAGE)

    def clean_html(self):
        html_parser = HTMLParser(self.raw_body)
        if html_parser.body:
            for tag in html_parser.css("script"):
                tag.decompose()
            for tag in html_parser.css("style"):
                tag.decompose()
            text = html_parser.body.text(separator=' ')
            self.clean_raw = text

    def remove_punct(self, text):
        text_no_punc = ''.join(
            [char for char in text.lower() if char not in string.punctuation])
        return text_no_punc

    def my_tokenize(self):

        text = self.remove_punct(self.clean_raw)
        w = re.split("\W+", text)

        w = [x for x in w if len(x) > 3]
        no_S = [word for word in w if word not in STOP_WORDS]
        text_clean_stem_stop = [ps.stem(word) for word in no_S]
        self.tokens = text_clean_stem_stop

    def tokenize_query(self, query):

        q = self.remove_punct(query)
        w = re.split("\W+", q)

        w = [x for x in w if len(x) > 3]
        no_S = [word for word in w if word not in STOP_WORDS]
        clean_q = [ps.stem(word) for word in no_S]
        return clean_q

    def read_doc(self, folder, docID):
        with open(folder + '/pages/' + str(docID)) as f:
            body = f.read()
        self.raw_body = body

    def get_tokens(self):
        return self.tokens

    def get_raw_body(self):
        return self.raw_body

    def get_clean_raw(self):
        return self.clean_raw

    @staticmethod
    def read_stop_words(file_name):  # "common_words"
        global STOP_WORDS
        stop_word = open(file_name).read()
        l = re.split("\W+", stop_word)
        STOP_WORDS.update(l)
# added
    # buidl a graph for all the docs

    def preprocess_documents(self):
        global link_extractor
        web_graph = graph.OptimizedDirectedGraph()

        with open('code_from_url_dict.pickle', 'rb') as handle:
            code_from_url = pickle.load(handle)
        for filename in range(self.n_pages):
            with open(self.FOLDER + '/pages/' + str(filename)) as f:
                doc_text = f.read()

            if doc_text is None:
                print('empty doc')
                print(filename)
                continue

            link_extractor = LinkExtractor(
                self.FOLDER, self.HOMEPAGE, self.DOMAIN_NAME)

            link_extractor.feed(doc_text)
            links = link_extractor.page_links()

            count = 0
            web_graph.add_node(int(filename))
            for url in links:
                if url in code_from_url:

                    count += 1
                    web_graph.add_edge(int(filename), code_from_url[url])
        return web_graph
