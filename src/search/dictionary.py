"""
This module provides the implementation of the Dictionary object and
its search methods.
"""
from collections import defaultdict
from src.db.crud import get_simplified_word, get_word_and_character
from typing import (
    ClassVar,
    DefaultDict,
    Generator,
    List,
    Tuple,
    Union,
    Sequence,
)

from sqlalchemy.orm import Session
from src.db.settings import SessionLocal
from src.schemas.structures import Word, Character
from src.db.models import Word as Word_model, Character as Character_model
from jieba import initialize, cut
from src.search.textutils import extract_chinese_characters


class Dictionary():
    """
    Dictionary object. Will handle connecting to the database and
    implement search, segment and other methods.
    """
    def __init__(self):
        initialize()
        self._dictionary: ClassVar[Session] = SessionLocal()
        self.search_term: str = ""
        self.segmented_words: Generator[str, None, None]
        self.dictionary_cache: DefaultDict[str, List[Union[Character, Word]]] = defaultdict(list)
        self.words_found: List[Union[Word, Character]] = []
        self.unknown_words: List[str] = []
        self.search_history: DefaultDict[str, int] = defaultdict(int)

    def segment_words(self) -> None:
        """
        This method segments the string into words using Jieba.
        """
        self.segmented_words = cut(self.search_term, cut_all=False)

    def search_chinese(self, search_term: str) -> None:
        """
        This method implements the search functionality for Chinese strings.
        It is what external programs will interact with.
        """
        # replace the current search term
        self.search_term = search_term
        # clear words found from previous search (still in cache)
        self.words_found.clear()
        # segment the search term
        self.segment_words()
        # iterate through each segmented word
        for word in self.segmented_words:
            # only look for it if it's not empty space
            if word.strip(): 
            # increase its value in the search_history
                self.search_history[word] += 1
                # first check to see if it's not cached
                if not self.dictionary_cache.get(word):
                    # check to see if it's a multiple character word, or single character word
                    if len(word) == 1:
                        word_character_results: List[
                            Tuple[Word_model, Character_model]
                        ] = get_word_and_character(self._dictionary, word)
                        # if the list is empty the next thing won't run
                        for word_result, character_result in word_character_results:
                            # use the Character structure
                            character: Character = self.combine_word_and_character(word_result, character_result)
                            self.words_found.append(character)
                            self.dictionary_cache[character.simplified].append(character)
                    else:
                        current_words = get_simplified_word(self._dictionary, word)
                        # for each of the words found, get their component characters
                        for result in current_words:
                            word = result.Word
                            component_characters = extract_chinese_characters(
                                word.simplified
                            )
                            current_word: Word = Word.from_orm(word)
                            for character, pinyin in zip(
                                component_characters, current_word.pinyin_accent.split()
                            ):
                                word_character_results = get_word_and_character(
                                    self._dictionary, character, pinyin_accent=pinyin
                                )
                                if len(word_character_results) == 0:
                                    word_character_results = get_word_and_character(
                                        self._dictionary, character
                                    )
                                for word_result, character_result in word_character_results:
                                    character: Character = self.combine_word_and_character(word_result, character_result)
                                    current_word.components.append(character)
                            self.words_found.append(current_word)
                            self.dictionary_cache[current_word.simplified].append(current_word)
                else:
                    cached_result = self.dictionary_cache.get(word)
                    self.words_found.extend(cached_result)
        # the result is stored in words_found

    @staticmethod
    def combine_word_and_character(
        word_result: Word_model, character_result: Character_model
    ) -> Character:
        character: Character = Character.from_orm(word_result)
        character.radical = character_result.radical
        character.decomposition = character_result.decomposition
        character.etymology = character_result.etymology
        return character

