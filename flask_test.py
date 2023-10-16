'''Unit Testing for Flask Application'''
import os
import unittest
from application import app

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# create class for form data
class FormData:
    '''Class to store form data for flask tests'''

    def __init__(
            self, known_texts=None, unknown_text=None, known_files=None,
            unknown_file=None, expected_output=200):
        '''Constructor for FormData class'''
        if known_texts is None:
            known_texts = []
        if known_files is None:
            known_files = []

        self.known_texts = known_texts
        self.unknown_text = unknown_text
        self.known_files = known_files
        self.unknown_file = unknown_file
        self.expected_output = expected_output

    def create_data(self) -> dict:
        '''create data to send to API using form data'''
        data = {
                'known_texts': self.known_texts,
                'known_files': self.known_files
        }
        if self.unknown_text:
            data['unknown_text'] = self.unknown_text
        if self.unknown_file:
            data['unknown_file'] = self.unknown_file

        return data

class FlaskTestCase(unittest.TestCase):
    '''Class to run test cases for flask app'''
    text_tests = [
        # known text + unknown text
        FormData(
            known_texts=['This is a test.'],
            unknown_text='This is a test.'
        ),
        # known text only
        FormData(known_texts=['This is a test.'], expected_output=401),
        # unknown text only
        FormData(unknown_text='This is a test.', expected_output=400),
    ]

    files_tests = [
        # known file + unknown file
        FormData(
            known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')
        ),
        # known file only
        FormData(
            known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            expected_output=401
        ),
        # unknown file only
        FormData(
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb'),
            expected_output=400
        )
    ]

    mix_tests = [
        # known text + known file + unknown file
        FormData(
            known_texts=['This is a test.'],
            known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')
        ),
        # known file + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_text='This is a test.'
        ),
        # known text + unknown file
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')
        ),
        # known text + unknown text + unknown file
        FormData(
            known_texts=['This is a test.'],
            unknown_text='This is a test.',
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')
        ),
        # known text + known file only
        FormData(
            known_texts=['This is a test.'],
            known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            expected_output=401
        ),
        # unknown file + unknown text only
        FormData(
            unknown_text='This is a test.',
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb'),
            expected_output=400
        ),
        # .pdf + .docx + .txt + unknown pdf
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/pdf_test01.pdf', 'rb'),
                open(BASE_DIR+'/test_files/docx_test01.docx', 'rb'),
                open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')
            ],
            unknown_file=open(BASE_DIR+'/test_files/pdf_test02.pdf', 'rb')
        ),
        # .pdf + .docx + .txt + unknown docx
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/pdf_test01.pdf', 'rb'),
                open(BASE_DIR+'/test_files/docx_test01.docx', 'rb'),
                open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_file=open(BASE_DIR+'/test_files/docx_test02.docx', 'rb')
        )
    ]

    corrupt_tests = [
        # corrupt pdf + unknown text
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/pdf_test_CORRUPT.pdf', 'rb')],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # corrupt docx + unknown text
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/docx_test_CORRUPT.docx', 'rb')],
            unknown_text='This is a test.', expected_output=400
        ),
        # corrupt txt + unknown text
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/txt_test_CORRUPT.txt', 'rb')],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # corrupt pdf + known files + known text + unknown text
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/pdf_test_CORRUPT.pdf', 'rb'),
                open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_file=open(BASE_DIR+'/test_files/pdf_test02.pdf', 'rb')
        ),
        # corrupt docx + known files + known text + unknown text
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/docx_test_CORRUPT.docx', 'rb'),
                open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_file=open(BASE_DIR+'/test_files/pdf_test02.pdf', 'rb')
        ),
        # corrupt txt + known files + known text + unknown text
        FormData(
            known_files=[
                open(BASE_DIR+'/test_files/txt_test_CORRUPT.txt', 'rb'),
                open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_file=open(BASE_DIR+'/test_files/pdf_test02.pdf', 'rb')
        ),
        # known text + corrupt unknown pdf
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(
                BASE_DIR+'/test_files/pdf_test_CORRUPT.pdf', 'rb'),
            expected_output=401
        ),
        # known text + corrupt unknown docx
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(
                BASE_DIR+'/test_files/docx_test_CORRUPT.docx', 'rb'),
            expected_output=401
        ),
        # known text + corrupt unknown txt
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(
                BASE_DIR+'/test_files/txt_test_CORRUPT.txt', 'rb'),
            expected_output=401
        )
    ]

    empty_tests = [
        # empty known text + unknown text
        FormData(
            known_texts=[''],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # known text + empty unknown text
        FormData(
            known_texts=['This is a test.'],
            unknown_text='',
            expected_output=401
        ),
        # empty known text + empty unknown text
        FormData(known_texts=[''], unknown_text='', expected_output=400),
        # empty known .pdf + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/pdf_test_EMPTY.pdf', 'rb')],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # empty known .docx + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/docx_test_EMPTY.docx', 'rb')],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # empty known .txt + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/txt_test_EMPTY.txt', 'rb')],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # empty known text + empty known files + unknown text
        FormData(
            known_texts=[''],
            known_files=[open(BASE_DIR+'/test_files/txt_test_EMPTY.txt', 'rb')],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # known text + empty known files + unknown text
        FormData(
            known_texts=['This is a test.'],
            known_files=[open(BASE_DIR+'/test_files/txt_test_EMPTY.txt', 'rb')],
            unknown_text='This is a test.'
        ),
        # empty known text + known files + unknown text
        FormData(
            known_texts=[''],
            known_files=[open(BASE_DIR+'/test_files/txt_test01.txt', 'rb')],
            unknown_text='This is a test.'
        ),
        # known text + empty unknown .pdf
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(BASE_DIR+'/test_files/pdf_test_EMPTY.pdf', 'rb'),
            expected_output=401
        ),
        # known text + empty unknown .docx
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(
                BASE_DIR+'/test_files/docx_test_EMPTY.docx', 'rb'),
            expected_output=401
        ),
        # known text + empty unknown .txt
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(BASE_DIR+'/test_files/txt_test_EMPTY.txt', 'rb'),
            expected_output=401
        ),
        # known text + unknown text + empty unknown file
        FormData(
            known_texts=['This is a test.'],
            unknown_text='This is a test.',
            unknown_file=open(BASE_DIR+'/test_files/txt_test_EMPTY.txt', 'rb'),
        ),
    ]

    misc_tests = [
        # non-pdf-docx-txt file + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/other_test.xml', 'rb')],
            unknown_text='This is a test.',
            expected_output=400
        ),
        # known text + non-pdf-docx-txt unknown file
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(BASE_DIR+'/test_files/other_test.xml', 'rb'),
            expected_output=401
        ),
        # known text + non-pdf-docx-txt file + known files + unknown text
        FormData(
            known_texts=['This is a test.'],
            known_files=[open(BASE_DIR+'/test_files/other_test.xml', 'rb')],
            unknown_text='This is a test.'
        ),
        # known text + unknown text + non-pdf-docx-txt unknown file
        FormData(
            known_texts=['This is a test.'],
            unknown_text='This is a test.',
            unknown_file=open(BASE_DIR+'/test_files/other_test.xml', 'rb')
        ),
        # unique ASCII known text + unknown text
        FormData(
            known_texts=[
                '''
📉🤨🔫😊😃😁🙂🤩😘😙😣😌😠🫢🤡🐹🐼🐲🐭👩🏽‍🦳👳🏽‍♀️🧔🏽‍♀️🧔🏽👩🏿‍🏭👩🏿‍🔬👩🏿‍💻👩🏿‍💼👩🏿‍🔧🫸🏿🫱🏿‍🫲🏼🫱🏿‍🫲🏼
(╬▔皿▔)╯[]~(￣▽￣)~*:P^o^^o^~_~~_~O.O¬_¬:-]T_T:S:-$:]*^____^*╰(*°▽°*)╯o(*^▽^*)┛
(￣y▽￣)╭ Ohohoho.....○( ＾皿＾)っ Hehehe…(p≧w≦q)(o゜▽゜)o☆(｡･∀･)ﾉﾞ（づ￣3￣）づ
╭❤️～（づ￣3￣）づ╭❤️～ヾ(^▽^*)))☆⌒(*＾-゜)v(｡･∀･)ﾉﾞo(*￣▽￣*)ブ(∪.∪ )...zzz
\\(@^0^@)/♪(´▽｀)（。＾▽＾）*★,°*:.☆(￣▽￣)/$:*.°★* 。ヽ(✿ﾟ▽ﾟ)ノ
⨷Ⅲ°↑ø—℗¡⁈⁔⁐ª⏒⁒⏔֏₽﷼₤ǎáBÃçėGĜɣǐíÑŉŃņŊŋŌṆŀŒɷɶɸÕŐŘśŦʅßŝŢɾɻǜǘǛýʏŹʒʭŴʑʢ↔↓↨↪↯↠↡↟↮↲
↬↸⇄⇥⇞⇔⇐⇉⇦⇧⇰⇷▨▦▧▪▮▯▬▤▣▦▥▢▸▶◀▰△◁▷◙▵◇◤◣◢◥◞◟◐◗◱◷◴◺◮◭◯◫◪■⁰⁷⁹
⅛⅛⅞↉⅟∃∀ⅧⅶⅨⅥ∈∋⋿ⅳ∋∊∑∝∎∓∰∮∱≀≋≕≜≯≸≴≨≫⊆⊃≽⊁⊛⊙⊓⊐⊏⊕⊘⊢⊞⊥⊭⊬⊯⊬⊶⊱⊻⊾⋁⋛⋜
⋥⋥⋢⋯⋰⋱⌗⏨⒎⒔⑨⑧⑤⋺⒐⑷⒀⒄⨀⨉⨐⨎⨂⨙⨟⨣⨔⨚⨭⨳⨱⨹⨶⨸⩑⩗⩄⩣⩝⩥⩫⩨⩷⪁⪈⪊⪋⪗⪛⪞⪜⪖⪪⫀⪫⪥⪼⫊
⫏⫕⫤⫟⫦⫨⫲⫸⫻ηαγνχΩϜᾸΆᾋἊᾍᾆΈέΈἚἠήᾔἰᾚἵἿΌἲὸΫΎὁὡὕῥὬὣᾬᾤϴϸϏͽϛϓ
🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧 🇦🇿 🇦🇺 🇦🇼 🇦🇴 🇦🇱 🇦🇲 🇦🇸 🇦🇹 🇦🇪 🇦🇬 🇦🇫 🇦🇮 🇦🇩 🇦🇷 🇧🇴 🇧🇷 🇧🇳 🇧🇲 🇧🇹 
🇧🇸 🇧🇾 🇧🇿 🇧🇼 🇧🇪 🇧🇫 🇧🇬 🇧🇭 🇧🇮 🇧🇯 🇧🇦 🇧🇧 🇧🇩 🇨🇻 🇨🇼 🇨🇺 🇨🇿 🇨🇾 🇨🇲 🇨🇰 🇨🇱 🇨🇷 🇨🇴 🇨🇩 🇨🇦 🇨🇬 🇨🇫 🇨🇮 🇨🇭 
🇩🇯 🇩🇲 🇩🇰 🇩🇴 🇩🇿 🇪🇹 🇪🇷 🇪🇬 🇪🇪 🇪🇨 🇫🇴 🇫🇮 🇫🇯 🇬🇹 🇬🇳 🇬🇲 🇬🇵 🇬🇷 🇬🇶 🇬🇺 🇬🇼 🇬🇾
اﺍﺎʾبﺏﺐﺒﺑʾت	ﺕﺖﺘهﻩﻪ	ﻬﻫʾ
龖釁𪚥爨 鬱饕餮𨽴 𤴒齉 龜纛鬻卖妻鬻女魑魅魍魎
            '''
            ],
            unknown_text='This is a test.'
        ),
        # known text + unique ASCII unknown text
        FormData(
            known_texts=['This is a test.'],
            unknown_text='''
📉🤨🔫😊😃😁🙂🤩😘😙😣😌😠🫢🤡🐹🐼🐲🐭👩🏽‍🦳👳🏽‍♀️🧔🏽‍♀️🧔🏽👩🏿‍🏭👩🏿‍🔬👩🏿‍💻👩🏿‍💼👩🏿‍🔧🫸🏿🫱🏿‍🫲🏼🫱🏿‍🫲🏼
(╬▔皿▔)╯[]~(￣▽￣)~*:P^o^^o^~_~~_~O.O¬_¬:-]T_T:S:-$:]*^____^*╰(*°▽°*)╯o(*^▽^*)┛(￣y▽￣)╭ Ohohoho.....○( ＾皿＾)っ Hehehe…(p≧w≦q)(o゜▽゜)o☆(｡･∀･)ﾉﾞ（づ￣3￣）づ╭❤️～（づ￣3￣）づ╭❤️～ヾ(^▽^*)))☆⌒(*＾-゜)v(｡･∀･)ﾉﾞo(*￣▽￣*)ブ(∪.∪ )...zzz\\(@^0^@)/♪(´▽｀)（。＾▽＾）*★,°*:.☆(￣▽￣)/$:*.°★* 。ヽ(✿ﾟ▽ﾟ)ノ
⨷Ⅲ°↑ø—℗¡⁈⁔⁐ª⏒⁒⏔֏₽﷼₤ǎáBÃçėGĜɣǐíÑŉŃņŊŋŌṆŀŒɷɶɸÕŐŘśŦʅßŝŢɾɻǜǘǛýʏŹʒʭŴʑʢ↔↓↨↪↯↠↡↟↮↲↬↸⇄⇥⇞⇔⇐⇉⇦⇧⇰⇷▨▦▧▪▮▯▬▤▣▦▥▢▸▶◀▰△◁▷◙▵◇◤◣◢◥◞◟◐◗◱◷◴◺◮◭◯◫◪■⁰⁷⁹⅛⅛⅞↉⅟∃∀ⅧⅶⅨⅥ∈∋⋿ⅳ∋∊∑∝∎∓∰∮∱≀≋≕≜≯≸≴≨≫⊆⊃≽⊁⊛⊙⊓⊐⊏⊕⊘⊢⊞⊥⊭⊬⊯⊬⊶⊱⊻⊾⋁⋛⋜⋥⋥⋢⋯⋰⋱⌗⏨⒎⒔⑨⑧⑤⋺⒐⑷⒀⒄⨀⨉⨐⨎⨂⨙⨟⨣⨔⨚⨭⨳⨱⨹⨶⨸⩑⩗⩄⩣⩝⩥⩫⩨⩷⪁⪈⪊⪋⪗⪛⪞⪜⪖⪪⫀⪫⪥⪼⫊⫏⫕⫤⫟⫦⫨⫲⫸⫻ηαγνχΩϜᾸΆᾋἊᾍᾆΈέΈἚἠήᾔἰᾚἵἿΌἲὸΫΎὁὡὕῥὬὣᾬᾤϴϸϏͽϛϓ
🇯🇵 🇰🇷 🇩🇪 🇨🇳 🇺🇸 🇫🇷 🇪🇸 🇮🇹 🇷🇺 🇬🇧 🇦🇿 🇦🇺 🇦🇼 🇦🇴 🇦🇱 🇦🇲 🇦🇸 🇦🇹 🇦🇪 🇦🇬 🇦🇫 🇦🇮 🇦🇩 🇦🇷 🇧🇴 🇧🇷 🇧🇳 🇧🇲 🇧🇹 🇧🇸 🇧🇾 🇧🇿 🇧🇼 🇧🇪 🇧🇫 🇧🇬 🇧🇭 🇧🇮 🇧🇯 🇧🇦 🇧🇧 🇧🇩 🇨🇻 🇨🇼 🇨🇺 🇨🇿 🇨🇾 🇨🇲 🇨🇰 🇨🇱 🇨🇷 🇨🇴 🇨🇩 🇨🇦 🇨🇬 🇨🇫 🇨🇮 🇨🇭 🇩🇯 🇩🇲 🇩🇰 🇩🇴 🇩🇿 🇪🇹 🇪🇷 🇪🇬 🇪🇪 🇪🇨 🇫🇴 🇫🇮 🇫🇯 🇬🇹 🇬🇳 🇬🇲 🇬🇵 🇬🇷 🇬🇶 🇬🇺 🇬🇼 🇬🇾
اﺍﺎʾبﺏﺐﺒﺑʾت	ﺕﺖﺘهﻩﻪ	ﻬﻫʾ
龖釁𪚥爨 鬱饕餮𨽴 𤴒齉 龜纛鬻卖妻鬻女魑魅魍魎
            '''
        ),
        # unique ASCII known .pdf file + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/pdf_test_UNIQUE.pdf', 'rb')],
            unknown_text='This is a test.'
        ),
        # unique ASCII known .docx file + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/docx_test_UNIQUE.docx', 'rb')],
            unknown_text='This is a test.'
        ),
        # unique ASCII known .txt file + unknown text
        FormData(
            known_files=[open(BASE_DIR+'/test_files/txt_test_UNIQUE.txt', 'rb')],
            unknown_text='This is a test.'
        )
    ]

    sim_test = (
        # making sure unknown file takes priority over unknown text
        FormData(
            known_texts=['This is a test.'],
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')
        ),
        FormData(
            known_texts=['This is a test.'],
            unknown_text='This is a test.',
            unknown_file=open(BASE_DIR+'/test_files/txt_test02.txt', 'rb')
        )
    )

    def setUp(self):
        '''Sets up the flask app for testing'''
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_texts(self):
        '''Tests with text only'''
        for form_data in self.text_tests:
            data = form_data.create_data()

            response = self.client.post(
                '/compare', data=data, content_type='multipart/form-data')

            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')

    def test_files(self):
        '''Tests with files only'''
        for form_data in self.files_tests:
            data = form_data.create_data()

            response = self.client.post(
                '/compare', data=data, content_type='multipart/form-data')

            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')

    def test_mix(self):
        '''Tests with a mix of text and files'''
        for form_data in self.mix_tests:
            data = form_data.create_data()

            response = self.client.post(
                '/compare', data=data, content_type='multipart/form-data')

            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')

    def test_corrupt(self):
        '''Tests with corrupt files'''
        for form_data in self.corrupt_tests:
            data = form_data.create_data()

            response = self.client.post(
                '/compare', data=data, content_type='multipart/form-data')

            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')

    def test_empty(self):
        '''Tests with files that have no content'''
        for form_data in self.empty_tests:
            data = form_data.create_data()

            response = self.client.post(
                '/compare', data=data, content_type='multipart/form-data')

            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')

    def test_misc(self):
        '''Miscelanious tests'''
        for form_data in self.misc_tests:
            data = form_data.create_data()

            response = self.client.post(
                '/compare', data=data, content_type='multipart/form-data')

            self.assertEqual(response.status_code, form_data.expected_output)
            self.assertEqual(response.content_type, 'application/json')

    def test_sim(self):
        '''Test to makesure responses are the same'''
        form_data1, form_data2 = self.sim_test
        # create data
        data1 = form_data1.create_data()
        data2 = form_data2.create_data()

        # create responses
        response1 = self.client.post(
            '/compare', data=data1, content_type='multipart/form-data')
        response2 = self.client.post(
            '/compare', data=data2, content_type='multipart/form-data')

        # make sure responses are the same
        self.assertEqual(response1.status_code, response2.status_code)
        self.assertEqual(response1.content_type, response2.content_type)
        self.assertEqual(response1.data, response2.data)
