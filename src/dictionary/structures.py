from abc import ABC, abstractmethod
from dictionary import Dictionary
'''
This file will contain the various lanuage structures used
in the program including Words, Sentences, Expressions, Radicals, etc.
'''





class Common(ABC):
    '''
    Common class.
    The Radical, Character, Word and Sentence classes will derive from it.
    Its methods are implemented as ABC methods that its children will have
    to define.
    '''
    def __init__(self, dictionary, **name):
        self.name = name['simplified']
        self.dict = dictionary
        self.definition = name['definition']
        self.stroke_diagram = None # not yet implemented
        self.simplified = name['simplified']
        self.traditional = name['traditional']


    @abstractmethod
    def list_components(self):
        pass

    @abstractmethod
    def list_words(self):
        pass

    @abstractmethod
    def list_sentences(self):
        pass

    @abstractmethod
    def get_traditional(self):
        pass

    @abstractmethod
    def get_simplified(self):
        pass

    @abstractmethod
    def get_pinyin(self, pinyin_type):
        pass


class Word(Common):
    def __init__(self, dictionary,**word):
        super().__init__(self, dictionary, **word)
        self.pinyin_num = word['pinyin_num']
        self.pinyin_accent = word['pinyin_accent']
        self.radical = None
          

class Character(Common):
    def __init__(self, **word):
        super().__init__(self, **word)
        # for HSK1-6 learners the attribute below will indicate
        # what level the character is part of
        self.hsk = None
        # the below will contain the type of character it is
        # in ['象形', '指事', '形声', '会意', '转注', '假借']
        # ie [pictograph, ideograph, determinative phonetic character,
        #     combined ideograph, transfer character, loan character]
        # not currently implemented
        self.character_type = None

    # the function below is not yet implemented, but will
    # return the component of a character based on the character type
    def list_components(self):
        return None

    # not yet implemented
    def list_words(self):
        return None

    # not yet implemented
    def list_sentences():
        return None

    def get_traditional(self):
        '''Converting simplified to traditional.

        If the characters are already in traditional,
        display a warning indicating so. Display a 
        notice if the two versions are equivalent.
        '''
        if (self.name == self.simplified) and (self.name == self.traditional):
            return "The simplified and traditional characters are the same."
        if (self.name != self.simplified) and (self.name == self.traditional):
            return "The current character is the traditional character."
        return self.traditional

    def get_simplified(self):
        '''Converting traditional to simplified.

        If the characters are already in simplified,
        display a warning indicating so. Display a 
        notice if the two versins are equivalent.
        '''
        if (self.name == self.simplified) and (self.name == self.traditional):
            return "The traditional and simplified characters are the same."
        if (self.name != self.traditional) and (self.name == self.simplified):
            return "The current character is the simplified character."
        return self.simplified

    def get_pinyin(self, pinyin_type='accent'):
        if pinyin_type == 'number':
            return self.pinyin_num
        return self.pinyin_accent

    # not yet implemented
    def draw():
        return None







class Word(Common):
    def __init__(self, dictionary, **word):
        super().__init__(dictionary, **word)
        self.pinyin_num = word['pinyin_num']
        self.pinyin_accent = word['pinyin_accent']
        self.definition = word['definition']
        # TODO: implement the radical attribute below
        self.radical = None
        self.characters = [i for i in self.name]

    def get_traditional(self):
        '''Converting simplified to traditional.

        If the characters are already in traditional,
        display a warning indicating so. Display a 
        notice if the two versions are equivalent.
        '''
        if (self.name == self.simplified) and (self.name == self.traditional):
            return "The simplified and traditional characters are the same."
        if (self.name != self.simplified) and (self.name == self.traditional):
            return "The current character is the traditional character."
        return self.traditional

    def get_simplified(self):
        '''Converting traditional to simplified.

        If the characters are already in simplified,
        display a warning indicating so. Display a 
        notice if the two versins are equivalent.
        '''
        if (self.name == self.simplified) and (self.name == self.traditional):
            return "The traditional and simplified characters are the same."
        if (self.name != self.traditional) and (self.name == self.simplified):
            return "The current character is the simplified character."
        return self.simplified

    def get_pinyin(self, pinyin_type='accent'):
        if pinyin_type == 'number':
            return self.pinyin_num
        return self.pinyin_accent

    def __str__(self):
        template = (
                f"Word: {self.name} \n"
                f"Traditional: {self.traditional} \n"
                f"Pinyin: {self.pinyin_accent} \n"
                f"Pinyin: {self.pinyin_num} \n"
                f"Definition: {self.definition}")
        return template

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.__class__ == other.__class__\
                and self.name == other.name\
                and self.pinyin_accent == other.pinyin_accent

    def list_components(self):
        return None

    def list_words(self):
        return None

    def list_sentences(self):
        return None
