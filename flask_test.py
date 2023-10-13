import unittest
from application import app
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

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

# create class for form data
class FormData(object):
    def __init__(self, known_texts=[], unknown_text=None, known_files=[], unknown_file=None, expected_output=200):
        self.known_texts = known_texts
        self.unknown_text = unknown_text
        self.known_files = known_files
        self.unknown_file = unknown_file
        self.expected_output = expected_output

class FlaskTestCase(unittest.TestCase):
    text_tests = [
        # known text + unknown text
        FormData(known_texts=['This is a test.'], unknown_text='This is a test.'),
        # known text only
        FormData(known_texts=['This is a test.'], expected_output=401),
        # unknown text only
        FormData(unknown_text='This is a test.', expected_output=400),
    ]
    
    files_tests = [
        # known file + unknown file
        FormData(known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')], unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')),
        # known file only
        FormData(known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')], expected_output=401),
        # unknown file only
        FormData(unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb'), expected_output=400)
    ]
    
    mix_tests = [
        # known text + known file + unknown file
        FormData(known_texts=['This is a test.'], known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')], unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')),
        # known file + unknown text
        FormData(known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')], unknown_text='This is a test.'),
        # known text + unknown file
        # CHECK it's the same as test case below (test unknown file priority)
        FormData(known_texts=['This is a test.'], unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')),
        # known text + unknown text + unknown file
        FormData(known_texts=['This is a test.'], unknown_text='This is a test.', unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')),
        # known text + known file only
        FormData(known_texts=['This is a test.'], known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')], expected_output=401),
        # unknown file + unknown text only
        FormData(unknown_text='This is a test.', unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb'), expected_output=400),
        # .pdf + .docx + .txt + unknown pdf
        FormData(
            known_files=[open(BASE_DIR+'/test_files/pdf_test01.txt', 'rb'),open(BASE_DIR+'/test_files/docx_test01.txt', 'rb'),open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')], 
            unknown_file=open(BASE_DIR+'/test_files/pdf_test02.txt', 'rb')
        ),
        # .pdf + .docx + .txt + unknown docx
        FormData(
            known_files=[open(BASE_DIR+'/test_files/pdf_test01.txt', 'rb'),open(BASE_DIR+'/test_files/docx_test01.txt', 'rb'),open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')], 
            unknown_file=open(BASE_DIR+'/test_files/docx_test02.txt', 'rb')
        )
    ]
    
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_texts(self):
        for form_data in self.text_tests:
            data = {
                'known_texts': form_data.known_texts,
                'known_files': form_data.known_files
            }
            if form_data.unknown_text:
                data['unknown_text'] = form_data.unknown_text
            if form_data.unknown_file:
                data['unknown_file'] = form_data.unknown_file

            response = self.client.post('/compare', data=data, content_type='multipart/form-data')
            
            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')
            
    def test_files(self):
        for form_data in self.files_tests:
            data = {
                'known_texts': form_data.known_texts,
                'known_files': form_data.known_files
            }
            if form_data.unknown_text:
                data['unknown_text'] = form_data.unknown_text
            if form_data.unknown_file:
                data['unknown_file'] = form_data.unknown_file

            response = self.client.post('/compare', data=data, content_type='multipart/form-data')
            
            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')
            
    def test_mix(self):
        for form_data in self.mix_tests:
            data = {
                'known_texts': form_data.known_texts,
                'known_files': form_data.known_files
            }
            if form_data.unknown_text:
                data['unknown_text'] = form_data.unknown_text
            if form_data.unknown_file:
                data['unknown_file'] = form_data.unknown_file

            response = self.client.post('/compare', data=data, content_type='multipart/form-data')
            
            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')