''' Functions for Document Processing and Response Simplification '''
import fitz
import docx2txt

def read_pdf(file):
    '''Extract text from .pdf file '''
    text = ""
    try:
        pdf_file = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf_file:
            text += page.get_text()
    except:
        return None
    return text


def read_doc(file):
    '''Extract text from .doc & .docx file'''
    try:
        text = docx2txt.process(file)
    except:
        return None
    return text


def process_file(file):
    '''Process files based on its type'''
    text = None
    if file.filename.endswith(".pdf"):
        text = read_pdf(file)
    if file.filename.endswith(".docx"):
        text = read_doc(file)
    if file.filename.endswith(".txt"):
        try:
            text = file.read().decode('UTF-8')
        except:
            return None

    return text


def proportion(val1: float, val2: float) -> float:
    '''Calculate proportion of a to b'''
    if val2 == 0:
        return 0

    return min(val1, val2)/max(val1, val2)*100


def list_pct(lst: list[float]) -> float:
    '''Convert list of floats to percentage'''
    for i, val in enumerate(lst):
        lst[i] = val*100
    return lst


def simplify_response(response: dict) -> dict:
    '''Simplify response from compare_mix_texts()'''
    simplified_response = {}

    simplified_response['w_sim'] = [None, response['w_sim'], response['w_sim']]

    # simplify list of punctuations to total count
    punct = ['.', ';', ':', '!', '?', '-', '(', ')', '\"', '\'', '`', '/']
    punct_c1 = 0
    punct_c2 = 0
    for punc in punct:
        punct_c1 += response[punc][0]
        punct_c2 += response[punc][1]
    simplified_response['punct_p'] = [
        punct_c1*100, punct_c2*100, proportion(punct_c1, punct_c2)
    ]

    # get sentence values
    simplified_response['avg_sent_l'] = response['avg_sentence_length'] + [
        proportion(response['avg_sentence_length'][0], response['avg_sentence_length'][1])]

    # get word values
    simplified_response['rare_word_p'] = list_pct(response['rare_word_count']) + [
        proportion(response['rare_word_count'][0], response['rare_word_count'][1])]
    simplified_response['long_word_p'] = list_pct(response['long_word_count']) + [
        proportion(response['long_word_count'][0], response['long_word_count'][1])]
    simplified_response['ttr'] = list_pct(
        response['ttr']) + [proportion(response['ttr'][0], response['ttr'][1])]
    simplified_response['word_count'] = response['word_count'] + \
        [proportion(response['word_count'][0], response['word_count'][1])]

    return simplified_response
