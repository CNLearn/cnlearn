'''
This script runs tests related to the extraction and conversion of CEDICT
to JSON and SQLite DB format.
'''

# import the necessary modules
import json
import sqlite3
from itertools import chain
import pytest
from extract import (convert_to_pinyin_clean,
                     convert_to_pinyin_accent,
                     convert_pinyin,
                     last_vowel)


@pytest.fixture
def json_dictionary():
    '''
    This fixture loads the JSON file as a python dictionary.
    '''
    with open('dict.json', 'r') as json_file:
        json_dict = json.load(json_file)
    return json_dict


@pytest.fixture
def cedict_file():
    '''
    This fixture counts the number of entries and unique (simplified)
    entries in the CEDICT file.
    '''
    set_of_simplified_entries = set()
    dictionary_entries = 0
    with open('cedict/cedict_1_0_ts_utf-8_mdbg.txt') as cedict_text_file:
        for line in cedict_text_file:
            dictionary_entries += 1
            set_of_simplified_entries.add(line.split()[1])
    unique_simplified_entries = len(set_of_simplified_entries)
    return (dictionary_entries, unique_simplified_entries)


@pytest.fixture
def sqlite_database():
    '''
    This fixture counts the number of entries and unique (simplified)
    entries in the SQLite database.
    '''
    # connect to the database
    connection = sqlite3.connect('dictionary.db')
    cursor = connection.cursor()
    n_entries = cursor.execute(
        'SELECT COUNT(*) FROM dict'
    ).fetchone()[0]
    n_unique = cursor.execute(
        'SELECT COUNT(DISTINCT simplified) FROM dict'
    ).fetchone()[0]
    # close the connection
    connection.close()
    return (n_entries, n_unique)


@pytest.fixture
def sqlite_shi_character():
    '''
    This fixture looks for the 是 character in the simplified column
    of the SQLite dictionary. There are two dictionary entries for it.
    It also looks at all the expressions containing 是 in them.
    '''
    # connect to the database
    connection = sqlite3.connect('dictionary.db')
    cursor = connection.cursor()
    single_shi_entries = cursor.execute(
        '''
        SELECT *
        FROM dict
        WHERE simplified="是"
        '''
    ).fetchall()
    shi_expression_entries = cursor.execute(
        '''
        SELECT *
        FROM dict
        WHERE simplified LIKE "%是%"
        ORDER BY
        LENGTH(simplified),
        CASE
            WHEN simplified LIKE "是%" THEN 1
            WHEN simplified LIKE "%是" THEN 3
            ELSE 2
        END
        '''
    ).fetchall()
    # close the connection
    connection.close()
    return (single_shi_entries, shi_expression_entries)


@pytest.fixture
def test_words_suite(json_dictionary):
    '''
    This fixture provides a list of dictionaries for a few random words
    extracted from the dictionary.
    '''
    test_word_1 = json_dictionary['一掬同情之泪'][0]
    test_word_2 = json_dictionary['3C'][0]
    test_word_3 = json_dictionary['USB记忆棒'][0]
    test_word_4 = json_dictionary['一哄而散'][0]
    test_word_5 = json_dictionary['不畏强权'][0]
    test_words = [test_word_1, test_word_2, test_word_3,
                  test_word_4, test_word_5]
    return test_words


def test_correct_number_of_words(json_dictionary,
                                 cedict_file,
                                 sqlite_database):
    '''
    Test whether the json_dictionary and the SQLite database includes all the
    terms in the original CEDICT file.
    '''
    n_entries_cedict, n_unique_simplified_cedict = cedict_file
    n_entries_sqlite, n_unique_simplified_sqlite = sqlite_database
    assert sum(
        len(value) for value in json_dictionary.values()
    ) == n_entries_cedict
    assert len(json_dictionary) == n_unique_simplified_cedict
    assert n_entries_sqlite == n_entries_cedict
    assert n_unique_simplified_sqlite == n_unique_simplified_cedict


def test_occurrences_of_shi_character(sqlite_shi_character, json_dictionary):
    '''
    Test if the 是 occurrences are separated in the database and the JSON
    dictionary.
    '''
    single_shi_entries_sql, shi_expression_entries_sql = sqlite_shi_character
    single_shi_entries_json = [tuple(i.values()) for i in json_dictionary['是']]
    shi_expression_entries_json = [
        value for key, value in json_dictionary.items() if '是' in key]
    shi_expression_entries_json = list(
        chain.from_iterable(shi_expression_entries_json))
    assert single_shi_entries_sql == single_shi_entries_json
    assert len(shi_expression_entries_sql) == len(shi_expression_entries_json)


def test_convert_to_pinyin_clean(test_words_suite):
    '''
    Tests if the pinyin with numbers to pinyin clean function works correctly.
    '''
    test_words = test_words_suite
    for word in test_words:
        for numbered_pinyin, clean_pinyin in zip(
                word['pinyin_num'].split(), word['pinyin_clean'].split()):
            assert convert_to_pinyin_clean(numbered_pinyin) == clean_pinyin


def test_convert_to_pinyin_accent(test_words_suite):
    '''
    Tests if the pinyin with numbers to pinyin with tone marks function
    works correctly.
    '''
    test_words = test_words_suite
    for word in test_words:
        for numbered_pinyin, accent_pinyin in zip(
                word['pinyin_num'].split(), word['pinyin_accent'].split()):
            assert convert_to_pinyin_accent(numbered_pinyin) == accent_pinyin


def test_convert_pinyin(test_words_suite):
    '''
    Tests if the overall conversion function with the flag works correctly.
    '''
    test_words = test_words_suite
    for word in test_words:
        for numbered_pinyin, clean_pinyin in zip(
                word['pinyin_num'].split(),
                word['pinyin_clean'].split()):
            assert convert_pinyin(numbered_pinyin, 'clean') == clean_pinyin
    for word in test_words:
        for numbered_pinyin, accent_pinyin in zip(
                word['pinyin_num'].split(),
                word['pinyin_accent'].split()):
            assert convert_pinyin(numbered_pinyin, 'accent') == accent_pinyin


@pytest.mark.xfail(raises=ValueError)
def test_convert_pinyin_exceptions_integer():
    '''
    Tests if passing a string or list of strings (such as an integer)
    will raise a ValueError.
    a ValueError.
    '''
    convert_pinyin(5, 'accent')


@pytest.mark.xfail(raises=ValueError)
def test_convert_pinyin_exceptions_wrong_flag():
    '''
    Test if passing a flag not `accent` or `clean` raises a ValueError.
    '''
    convert_pinyin(5, 'country')


def test_last_vowel():
    '''
    Tests the last vowel function.
    '''
    assert last_vowel('woah') == 2
    assert last_vowel('hao') == 2
    assert last_vowel('kong') == 1
    assert last_vowel('3 P') is None
    assert last_vowel('456') is None
