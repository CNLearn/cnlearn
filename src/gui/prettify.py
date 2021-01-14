'''This module contains functions to make text pretty.
So shallow, I know.'''

def colorise_characters_and_pinyin(word):
    color_dictionary = {1: '00FF00',
                        2: '00B3FF',
                        3: 'FFEF00',
                        4: 'FF0000',
                        5: 'E600FF'}
    characters = word['simplified']
    pinyin = word['pinyin_num']
    pinyin_accent = word['pinyin']
    colorised = '[size=40sp][b]'
    for character, pinyin_ind in zip(characters, pinyin.split()):
        try:
            color_number = int(pinyin_ind[-1])
            color = color_dictionary[color_number]
        except ValueError:
            color = color_dictionary[5]
        colorised += f'[color={color}]{character}[/color]'
    colorised += '[/b][/size]  '
    for pinyin_word, pinyin_ind in zip(pinyin_accent.split(), pinyin.split()):
        try:
            color_number = int(pinyin_ind[-1])
            color = color_dictionary[color_number]
        except ValueError:
            color = color_dictionary[5]
        colorised += f'[color={color}]{pinyin_word}[/color]'
    return colorised



def pretty_definition(word):
    definition = word['definition']
    definitions = ''
    for i, j in enumerate([i.lstrip() for i in definition.split(';')]):
        definitions += f"{i+1:>2}: {j}\n"
    header = colorise_characters_and_pinyin(word)
    definitions = "[size=36sp][b]Definition:[/b][/size]\n" + definitions 
    return (header, definitions)