from typing import Dict, List, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
from enum import Enum, IntEnum


class CharacterType(str, Enum):
    象形 = '象形'
    指事 = '指事'
    形声 = '形声'
    会意 = '会意'
    转注 = '转注'
    假借 = '假借'


class HSKLevel(IntEnum):
    hsk_1: 1
    hsk_2: 2
    hsk_3: 3
    hsk_4: 4
    hsk_5: 5
    hsk_6: 6


class Common(BaseModel, ABC):
    """
    Common class.
    The Character, Word and Sentence classes will derive form it.
    Its methods are implemented as ABC methods that its children will have
    to define.
    """

    id: Optional[int]
    definitions: str
    stroke_diagram: Optional[str] # not yet implemented, will likely be a reference
    # to a SVG file (e.g. 37683.svg)
    simplified: str
    traditional: str
    pinyin_num: str
    pinyin_accent: str
    pinyin_clean: str
    also_pronounced: Optional[str]
    also_written: Optional[str]
    classifiers: Optional[str]
    frequency: int


    class Config:
        orm_mode = True

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




class Radical(BaseModel):
    name: Optional[str]
    components: List[str]


class Character(Common):
    character_type: Optional[CharacterType] # optional for now
    # radical: Optional[Radical] # optional for now
    radical: Optional[str]
    # decomposition: Optional[List[str]] # optional for now
    decomposition: Optional[str]
    etymology: Optional[Dict]

    def list_components(self) -> None:
        """
        Not yet implemented.
        Will return the components of a character based on the
        character type.
        """
        return None

    def list_words(self) -> None:
        """
        Not yet implemented.
        Will returns words containing this character.
        """
        # TODO: implement this first
        return None

    def list_sentences(self) -> None:
        """
        Not yet implemented.
        Will return sentences containing this character.
        """
        return None

    def get_traditional(self) -> str:
        """
        Returns the traditional version of the character.
        """
        return self.traditional
    
    def get_simplified(self) -> str:
        """
        Returns the simplified version of the character.
        """
        return self.simplified

    def get_pinyin(self, pinyin_type = 'accent') -> str:
        """
        Returns the pinyin representation of the character:
        - pinyin_type is a string argument, 'accent' default
        There is a choice between 'accent' and 'num'
        """
        if pinyin_type == 'num':
            return self.pinyin_num
        elif pinyin_type == 'clean':
            return self.pinyin_clean
        return self.pinyin_accent


class Word(Common):
    pinyin_no_spaces: str
    components: Optional[List[Character]]
    radical: Optional[Radical] # if it's one character word will have
    hsk: Optional[HSKLevel] # some words won't have this
    

    def list_components(self) -> List[Character]:
        """
        Returns the Characters making up this word."
        """
        return self.components

    def list_words(self) -> None:
        """
        Not yet implemented.
        Returns longer words containing this Word.
        """
        return None

    def list_sentences(self) -> None:
        """
        Not yet implemented.
        Retrusn sentences containing this Word.
        """
        return None

    def get_traditional(self) -> str:
        """
        Returns the traditional version of the Word.
        """
        return self.traditional

    def get_simplified(self) -> str:
        """
        Returns the simplified version of the Word.
        """
        return self.simplified

    def get_pinyin(self, pinyin_type = 'accent') -> str:
        """
        Returns the pinyin representation of the Word:
        - pinyin_type is a string argument, 'accent' default
        There is a choice between 'accent' and 'num' and 'clean'
        """
        if pinyin_type == 'num':
            return self.pinyin_num
        elif pinyin_type == 'clean':
            return self.pinyin_clean
        return self.pinyin_accent

