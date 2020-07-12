# used for saving the dictionary to json format
import io
import json
# used to create a python dictionary that can have duplicate keys
from collections import defaultdict
# used for saving the dictionary to a database
import sqlite3


# define the file where the CEDICT is stored
filename = 'cedict/cedict_1_0_ts_utf-8_mdbg.txt'


# the list below is a list of vowels that appear in the CEDICT pinyin
vowels = ['a', 'e', 'i', 'o', 'u', 'u:', 'A', 'E', 'I', 'O', 'U', 'U:']
# the dictionary below will convert the vowels to vowels with accents
# depening on their tone as specified at the end of the word
vowel_dict = {1: ['ā', 'ē', 'ī', 'ō', 'ū', 'ǖ', 'Ā', 'Ē', 'Ī', 'Ō', 'Ū', 'Ǖ'],
              2: ['á', 'é', 'í', 'ó', 'ú', 'ǘ', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ǘ'],
              3: ['ǎ', 'ě', 'ǐ', 'ǒ', 'ǔ', 'ǚ', 'Ǎ', 'Ě', 'Ǐ', 'Ǒ', 'Ǔ', 'Ǚ'],
              4: ['à', 'è', 'ì', 'ò', 'ù', 'ǜ', 'À', 'È', 'Ì', 'Ò', 'Ù', 'Ǜ'],
              5: ['a', 'e', 'i', 'o', 'u', 'ü', 'A', 'E', 'I', 'O', 'U', 'Ü']}


# the function below converts a pinyin with numbers to pinyin with accents
def convert_to_pinyin_accent(word: str):
    tone = ord(word[-1])-48
    if (tone > 0 and tone < 6):
        word_without_tone = word[0:-1]
        if (tone < 5):
            search_list = ['a', 'e', 'ou']
            for c in search_list:
                if c in word_without_tone:
                    pos = word_without_tone.find(c)
            else:  # if none of the above are found, the tone mark goes on the last vowel
                pos = last_vowel(word_without_tone)

            try:
                pos
            except NameError:
                pos = None
            if pos is not None:
                # check if followed by : to change it accordingly
                try:
                    word_without_tone[pos+1]
                    if word_without_tone[pos+1] == ":":
                        toReplace = word_without_tone[pos:pos+2]
                    else:
                        toReplace = word_without_tone[pos:pos+1]
                except IndexError:
                    toReplace = word_without_tone[pos:pos+1]
                pinyin_word = word_without_tone.replace(
                    toReplace, vowel_dict[tone][vowels.index(toReplace)])
        else:
            pinyin_word = word_without_tone.replace('u:', 'ü')
            pinyin_word = word_without_tone.replace('U:', 'Ü')
    else:
        pinyin_word = word
    try:
        pinyin_word
    except NameError:
        pinyin_word = None
    return pinyin_word

# the function below converts from pinyin with numbers to just pinyin
def convert_to_pinyin_clean(word: str):
    tone = ord(word[-1])-48
    if (tone > 0 and tone < 6):
        pinyin_clean = word[0:-1]
    else:
        pinyin_clean = word
    try:
        pinyin_clean
    except NameError:
        pinyin_clean = None
    return pinyin_clean


def last_vowel(word):
    # another way to reverse a string is ''.join(list(reversed(word)))
    reverse_word = word[::-1]
    for i in reverse_word:
        for c in vowels:
            if c in i:
                return word.find(c)


# def convert_everything_to_pinyin_accent(item):
#     if isinstance(item, str):
#         return convert_to_pinyin_accent(item)
#     elif isinstance(item, list):
#         pinyin_accent = []
#         for i in item:
#             pinyin_accent.append(convert_to_pinyin_accent(i))
#         return pinyin_accent



def convert_pinyin(item, flag):
    if flag in ['accent', 'clean']:
        if isinstance(item, str):
            if flag == 'accent':
                return convert_to_pinyin_accent(item)
            elif flag == 'clean':
                return convert_to_pinyin_clean(item)
            else:
                raise ValueError
        elif isinstance(item, list):
            pinyin_list = []
            for i in item:
                pinyin_list.append(convert_pinyin(i, flag))
            return pinyin_list
    else:
        return "Flag must be 'accent' or 'clean'"



''' 
Now let's create a SQLite database and add the same information as above.
Eventually this part will go into the parse_line function above so that 
we do not do multiple iterations.
We need to create a database and its schema, and then insert all the
information into it.s
'''


class SQLiteDatabase(object):
    '''
    This object will contain all the functionality related to the SQLite DB.
    '''

    def __init__(self, db_name: str):
        self.db = db_name
        self.opened = False
        self.cursor = None

    def connect(self):
        ''' open the connection to the database.
        If the file does not exist, it will be created automatically.'''
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.opened = True

    def disconnect(self):
        ''' close the connection to the database '''
        if self.opened:
            self.connection.commit()
            self.cursor.close()
            self.opened = False
        else:
            return "You are not connected to the table."

    def create_table_schema(self):
        if self.opened:
            self.cursor.execute('''CREATE TABLE dict
            (simplified VARCHAR(50),
            pinyin_num VARCHAR(50),
            pinyin_accent VARCHAR(50),
            pinyin_clean VARCHAR(50),
            definitions VARCHAR(500)
            );
            ''')
            #CONSTRAINT pk PRIMARY KEY (simplified, pinyin_num, definitions)
            self.connection.commit()

        else:
            self.connect()
            self.create_table_schema()

    def update_db(self, data):
        if self.opened:
            statement = '''
            INSERT INTO dict 
            (simplified, pinyin_num, pinyin_accent, pinyin_clean, definitions)
            VALUES (?,?,?,?,?);'''
            self.cursor.execute(statement, data)
            self.connection.commit()

        else:
            self.connect()
            self.update_db(data)


'''
Instead of using a Python dictionary, let's now use a defaultdict that can
store multiple values in a list for a key. Why do I need to do that? Well,
I made silly mistake. One of the harder things about learning Chinese are
characters that have multiple pronunciations. They are written the same
but pronounced differently. So what my original script did was everytime
it processed a line, if there was a character it had already seen before, it
would then replace the information for it with the one it had just seen.
We want to be able to access all the meanings, so am using a defaultdict now.
'''
dictionary = defaultdict(list)
# create a DB object
db = SQLiteDatabase('dictionary.db')
# open the connection
db.connect()
# create the schema
db.create_table_schema()


def parse_line(line, dictionary, db_object):
    traditional = line.split(' ')[0]
    simplified = line.split(' ')[1]
    pinyin = line[line.find('[')+1:line.find(']')]
    definitions = '; '.join(line[line.find('/')+1:line.rfind('/')].split("/"))
    try:
        pinyin_accent = " ".join(convert_pinyin(pinyin.split(), 'accent'))
        pinyin_clean = " ".join(convert_pinyin(pinyin.split(), 'clean'))
        #pinyin_accent = " ".join(convert_everything_to_pinyin(pinyin.split()))
    except TypeError:
        pinyin_accent = ""
        pinyin_clean = ""

    dictionary[simplified].append({"simplified": simplified,
                                   "traditional": traditional,
                                   "pinyin_num": pinyin,
                                   "pinyin_accent": pinyin_accent,
                                   "pinyin_clean": pinyin_clean,
                                   "definition": definitions})
    # add the same data to the database
    db.update_db(
         data=(simplified, pinyin, pinyin_accent, pinyin_clean, definitions))
         
with open(filename, "r", encoding='utf-8') as f:
    for line in f:
        parse_line(line, dictionary, db)
    # close the database connection when done
    db.disconnect()


with io.open('dict.json', 'w', encoding='utf8') as json_file:
    json.dump(dictionary, json_file, ensure_ascii=False)
