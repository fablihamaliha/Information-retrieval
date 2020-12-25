import easygui as eg
import webbrowser


def ask_query():
    #img = "ryerson_logo.png"
    msg = "Enter your query"
    title = "Query"
    #response = eg.enterbox(msg, title, image=img)
    response = eg.enterbox(msg, title)
    return response


def open_website(url):
    webbrowser.open(url.split()[0], new=2, autoraise=True)


def handle_show_no_resualts():
    msg = ""
    msg = "No result"
    title = "search results"
    eg.msgbox("No result", ok_button="search")
    return False


def display_query_results(docs_list, url_from_code, query_tokens):
    msg = ""
    title = ""
    url_list = []
    msg = "Preprocessed query: "+str(query_tokens)+"\ndouble click or select and press ok" \
                                                   " to open the web page in a new tab of your default browser"

    title = "search results"
    url_list = [str(url_from_code[code]) for code in docs_list]
    choice = eg.choicebox(msg, title, url_list)
    return choice
