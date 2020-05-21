import unittest
from search import Search
from structures import Word
from dictionary import Dictionary

class search_tests(unittest.TestCase):
    def setUp(self):
        self.dictionary = Dictionary()
        self.search_term = "不好意思谁是鸡吧388是hahsaQ三3Q不好意思"
        self.search_object = Search(dictionary=self.dictionary)
        self.search_object.search(search_term  = self.search_term,
                gui_flag=True)

    def test_word_object_creation(self):
        for word in self.search_object.search_words:
            self.assertTrue(isinstance(word,Word))
        for word in self.search_object.unknown_words:
            self.assertFalse(isinstance(word,Word))
        self.assertEqual(len(self.search_object.search_words), 7)

    def test_some_words(self):
        word_0, word_1, word_2, word_3, word_4, word_5, word_6 = self.search_object.search_words
        self.assertEqual(len(word_0.characters),4)
        self.assertEqual(word_3.name, '鸡')
        self.assertIs(word_2.dict, word_6.dict)

    def test_unknown_words(self):
        self.assertEqual(len(self.search_object.unknown_words),2)

    def tearDown(self):
        self.search_term = None
        del(self.search_object)
        del(self.dictionary)


