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
    if file.filename.endswith(".pdf"):
        text = read_pdf(file)
        return text
    elif file.filename.endswith(".docx"):
        text = read_doc(file)
        return text
    elif file.filename.endswith(".txt"):
        text = file.read().decode('UTF-8')
        return text
    
    
def proportion(a: float, b:float) -> float:
    '''Calculate proportion of a to b'''
    if b == 0:
        return 0
    else:
        return min(a,b)/max(a,b)*100
    
def list_pct(lst: list[float]) -> float:
    for i in range(len(lst)):
        lst[i] = lst[i]*100
    return lst
    
def simplify_response(response: dict) -> dict:
    '''Simplify response from compare_mix_texts()'''
    simplified_response = {}
    
    simplified_response['w_sim'] = [None,response['w_sim'],response['w_sim']]
    
    # simplify list of punctuations to total count
    punct = ['.',';',':','!','?','-','(',')','\"','\'','`','/']
    punct_c1 = 0
    punct_c2 = 0
    for p in punct:
        punct_c1 += response[p][0]
        punct_c2 += response[p][1]
    simplified_response['punct_p'] = [punct_c1*100, punct_c2*100, proportion(punct_c1, punct_c2)]
    
    # get sentence values
    simplified_response['avg_sent_l'] = response['avg_sentence_length'] + [proportion(response['avg_sentence_length'][0], response['avg_sentence_length'][1])]
    simplified_response['sent_over_avg'] = list_pct(response['sentences_over_avg']) + [proportion(response['sentences_over_avg'][0], response['sentences_over_avg'][1])]
    simplified_response['sent_under_avg'] = list_pct(response['sentences_under_avg']) + [proportion(response['sentences_under_avg'][0], response['sentences_under_avg'][1])]
    
    # get word values
    simplified_response['rare_word_p'] = list_pct(response['rare_word_count']) + [proportion(response['rare_word_count'][0], response['rare_word_count'][1])]
    simplified_response['long_word_p'] = list_pct(response['long_word_count']) + [proportion(response['long_word_count'][0], response['long_word_count'][1])]
    simplified_response['words_over_avg'] = list_pct(response['words_over_avg_length']) + [proportion(response['words_over_avg_length'][0], response['words_over_avg_length'][1])]
    simplified_response['words_under_avg'] = list_pct(response['words_under_avg_length']) + [proportion(response['words_under_avg_length'][0], response['words_under_avg_length'][1])]
    simplified_response['ttr'] = list_pct(response['ttr']) + [proportion(response['ttr'][0], response['ttr'][1])]
    simplified_response['word_count'] = response['word_count'] + [proportion(response['word_count'][0], response['word_count'][1])]
    
    return simplified_response