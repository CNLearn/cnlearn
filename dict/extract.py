import json
filename = 'cedict/cedict_1_0_ts_utf-8_mdbg.txt'






vowels   = ['a', 'e', 'i', 'o', 'u', 'u:', 'A', 'E', 'I', 'O', 'U', 'U:']
vowel_dict = {1: ['ā', 'ē', 'ī', 'ō', 'ū', 'ǖ', 'Ā', 'Ē', 'Ī', 'Ō', 'Ū', 'Ǖ'], 2:['á', 'é', 'í', 'ó', 'ú', 'ǘ', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ǘ'], 3:['ǎ', 'ě', 'ǐ', 'ǒ', 'ǔ', 'ǚ', 'Ǎ', 'Ě', 'Ǐ', 'Ǒ', 'Ǔ', 'Ǚ'], 4:['à', 'è', 'ì', 'ò', 'ù', 'ǜ', 'À', 'È', 'Ì', 'Ò', 'Ù', 'Ǜ'], 5:['a', 'e', 'i', 'o', 'u', 'ü', 'A', 'E', 'I', 'O', 'U', 'Ü']}


def convert_to_pinyin_accent(word):
    tone = ord(word[-1])-48
    if (tone > 0 and tone < 6):
        word_without_tone = word[0:-1]
        if (tone < 5):
            search_list = ['a', 'e', 'ou']
            for c in search_list:
                if c in word_without_tone:
                    pos = word_without_tone.find(c)
            else: # if none of the above are found, the tone mark goes on the last vowel
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
                pinyin_word = word_without_tone.replace(toReplace,vowel_dict[tone][vowels.index(toReplace)])
        else:
            pinyin_word = word_without_tone.replace('u:','ü')
            pinyin_word = word_without_tone.replace('U:','Ü')
    else:
        pinyin_word = word
    try:
        pinyin_word
    except NameError:
        pinyin_word = None
    return pinyin_word

def last_vowel(word):
    #another way to reverse a string is ''.join(list(reversed(word)))
    reverse_word = word[::-1]
    for i in reverse_word:
        for c in vowels:
            if c in i:
                return word.find(c)



def convert_everything_to_pinyin(item):
    if isinstance(item,str):
        return convert_to_pinyin_accent(item)
    elif isinstance(item,list):
        pinyin_accent = []
        for i in item:
            pinyin_accent.append(convert_to_pinyin_accent(i))
        return pinyin_accent




def parse_line(line):
    traditional = line.split(' ')[0]
    simplified = line.split(' ')[1]
    pinyin = line[line.find('[')+1:line.find(']')]
    definitions = '; '.join(line[line.find('/')+1:line.rfind('/')].split("/"))
    dictionary[simplified] = {"simplified":simplified, "traditional":traditional,"pinyin_num" :pinyin,  "definition" :definitions}

  

dictionary = {}
with open(filename,"r",encoding = 'utf-8') as f:
    for line in f:
        parse_line(line)
       


for word, information in dictionary.items():
    try:
        information['pinyin_accent'] = " ".join(convert_everything_to_pinyin(information['pinyin_num'].split()))
    except TypeError:
        information['pinyin_accent'] = ''
import io

#with open('finalDict.json', 'w') as f:
#    json.dump(dictionary, f).encode('utf8')

with io.open('dict.json', 'w', encoding='utf8') as json_file:
    json.dump(dictionary, json_file, ensure_ascii=False)
