from collections import defaultdict
from json import load
from structures import Word
from dictionary import Dictionary
from jieba import cut
import jieba
jieba.initialize()

class Search(object):
    """ Search object. Will handle the actual dictionary
    search and implements a few useful methods and attributs.

    Attributes include:
    - search history (set)
    - search history frequency (might be useful when learning
    a language to know how often you've looked at a word) implemented
    as a default dictionary
    - actually the two above will be combined
    - a list of the unique words that were found in the current session
    - a list of the unique words that were not found in the current session

    Methods include:
    - search
    - list history
    - list words in the current search string
    - and others (this list will be updated as the project progresses)
    """

    def __init__(self, dictionary):
        # initialise its dictionary
        self.dictionary = dictionary.dict
        self.search_term = None
        self.search_words = list() # will be a list of word objects
        self.unknown_words = list()
        # the search history is implemented as a default dictionary
        # with int as its default type. that way, all the default
        # values are 0 and don't have to check if an item exists
        # in the dictionary saving an if/try condition.
        self.search_history = defaultdict(int)

    def search(self, search_term, all_flag=False, gui_flag=False):
        self.search_term = search_term
        # now let's use jieba's segmenter to cut the string into words
        self.search_segmented = cut(self.search_term, cut_all=all_flag)
        # the above is a generator
        for i in self.search_segmented:
            try:
                word = Word(self.dictionary, **self.dictionary[i])
                if word not in self.search_words:
                    self.search_words.append(word)
            except KeyError:
                if i not in self.unknown_words:
                    self.unknown_words.append(i)
        if not gui_flag:
            for word in self.search_words:
                print(word)





