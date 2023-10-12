import requests
import os

# create class for form data
class FormData(object):
    def __init__(self, known_texts=[], unknown_text=None, known_files=[], unknown_file=None, expected_output=200):
        self.known_texts = known_texts
        self.unknown_text = unknown_text
        self.known_files = known_files
        self.unknown_file = unknown_file
        self.expected_output = expected_output
        
# create a function which connects to AI with the url http://3.26.213.177:5000/ and returns True if output matches expected output
def test_compare(url: str, form_data: FormData):
    # make data a multipart/form-data from FormData
    data = {}
    
    if form_data.known_texts:
        data['known_texts'] = form_data.known_texts
    if form_data.unknown_text:
        data['unknown_text'] = form_data.unknown_text
        
    files = form_data.known_files
    if form_data.unknown_file:
         files += [form_data.unknown_file]
        
    response = requests.post(url, data=data, files=files)
    
    return response.status_code == form_data.expected_output


if __name__ == '__main__':
    # ASSUMPTION FILE IS .txt UNLESS SPECIFIED
    url = 'https://wxqjx4px-5000.auc1.devtunnels.ms/compare'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    
    tests = []
    
    ### ========== ALL TEST CASES ========== ###
    
    # ============ Text Test Cases =========== #
    # known text + unknown text
    tests.append(FormData(known_texts=['This is a test.'], unknown_text='This is a test.'))
    
    # known text only
    tests.append(FormData(known_texts=['This is a test.'], expected_output=401))
    
    # unknown text only
    tests.append(FormData(unknown_text='This is a test.', expected_output=400))
    # ======================================== #
    
    # ============ File Test Cases =========== #
    # known file + unknown file
    tests.append(FormData(
        known_files = [('known_files', ('txt_test01.txt', open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')))], 
        unknown_file = ('unknown_file', ('txt_test02.txt', open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')))
    ))
    
    # known file only
    
    # unknown file only
    
    # ======================================== #
    
    # =========== Mixed Test Cases =========== #
    # known text + known file + unknown file
    # CHECK it's the same as test case above (test unknown file priority)
     
    # known text + unknown text + unknown file
    
    # known text + known file only
    
    # unknown file + unknown text only
    
    # .pdf + .docx + .txt + unknown pdf
    
    # .pdf + .docx + .txt + unknown docx
    
    # ======================================== #
    
    # ========== Corrupt Test Cases ========== #
    # corrupt pdf + unknown text
    
    # corrupt docx + unknown text
    
    # corrupt txt + unknown text
    
    # corrupt pdf + known files + known text + unknown text
    
    # corrupt docx + known files + known text + unknown text
    
    # corrupt txt + known files + known text + unknown text
    
    # known text + corrupt unknown pdf
    
    # known text + corrupt unknown docx
    
    # known text + corrupt unknown txt
    
    # ======================================== #
    
    # =========== Empty Test Cases =========== #
    # empty known text + unknown text
    
    # known text + empty unknown text
    
    # empty known text + empty unknown text
    
    # empty known .pdf + unknown text
    
    # empty known .docx + unknown text
    
    # empty known .txt + unknown text
    
    # empty known text + empty known files + unknown text
    
    # known text + empty known files + unknown text
    
    # empty known text + known files + unknown text
    
    # known text + empty unknown .pdf
    
    # known text + empty unknown .docx
    
    # known text + empty unknown .txt
    
    # known text + unknown text + empty unknown file
    
    # ======================================== #
    
    # =========== Misc. Test Cases =========== #
    # non-pdf-docx-txt file + unknown text
    
    # known text + non-pdf-docx-txt unknown file
    
    # known text + non-pdf-docx-txt file + known files + unknown text
    
    # known text + unknown text + non-pdf-docx-txt unknown file
    
    # unique ASCII known text + unknown text
    
    # known text + unique ASCII unknown text
    
    # unique ASCII known .pdf file + unknown text
    
    # unique ASCII known .docx file + unknown text
    
    # unique ASCII known .txt file + unknown text 
    
    # ======================================== #
    ### ==================================== ###
    
    for test in tests:
        if not test_compare(url, test):
            print('Test Failed')
            break