from typing import List
from cnlearn.db.settings import SessionLocal
from cnlearn.db.crud import (
    get_simplified_character,
    get_simplified_word_containing_char,
    get_simplified_word,
    get_word_and_character,
)
from sqlalchemy.orm import Session
from sqlalchemy.engine import Row
from cnlearn.db.models import Word, Character
import pytest


@pytest.fixture
def db() -> Session:
    """
    Returns a reusable database session.
    """
    session: Session = SessionLocal()
    return session


# parametrising beacause I will add more cases
@pytest.mark.parametrize(
    "simplified,pinyin_num,pinyin_accent,definitions,frequency",
    [("贼", "zei2", "zéi", "thief; traitor; wily; deceitful; evil; extremely", 3254)],
)
def test_get_simplified_no_pinyin(
    db: Session,
    simplified: str,
    pinyin_num: str,
    pinyin_accent: str,
    definitions: str,
    frequency: int,
):
    word_result: List[Row] = get_simplified_word(db, simplified=simplified)
    assert len(word_result) == 1
    word: Word = word_result[0].Word
    assert isinstance(word, Word)
    assert word.simplified == simplified
    assert word.pinyin_num == pinyin_num
    assert word.pinyin_accent == pinyin_accent
    assert word.definitions == definitions
    assert word.frequency == frequency


def test_get_simplified_no_pinyin_mutliple_results(db: Session):
    word_result: List[Row] = get_simplified_word(db, simplified="好")
    assert len(word_result) == 2
    hao1: Word = word_result[0].Word
    hao2: Word = word_result[1].Word
    assert isinstance(hao1, Word)
    assert isinstance(hao2, Word)


def test_get_word_and_character_no_pinyin(db: Session):
    word_character_results: List[Row] = get_word_and_character(db, simplified="好")
    assert len(word_character_results) == 2
    word_1: Word = word_character_results[0].Word
    word_2: Word = word_character_results[1].Word
    character_1: Character = word_character_results[0].Character
    character_2: Character = word_character_results[1].Character
    assert isinstance(word_1, Word)
    assert isinstance(word_2, Word)
    assert isinstance(character_1, Character)
    assert isinstance(character_2, Character)


def test_get_word_and_character_with_clean_pinyin(db: Session):
    word_character_results: Row = get_word_and_character(
        db, simplified="好", pinyin_clean="hao"
    )
    assert len(word_character_results) == 2
    word_1: Word = word_character_results[0].Word
    word_2: Word = word_character_results[1].Word
    character_1: Character = word_character_results[0].Character
    character_2: Character = word_character_results[1].Character
    assert isinstance(word_1, Word)
    assert isinstance(word_2, Word)
    assert isinstance(character_1, Character)
    assert isinstance(character_2, Character)


def test_get_simplified_character(db: Session):
    character_result: Row = get_simplified_character(db, simplified="好")
    character: Character = character_result.Character
    assert isinstance(character, Character)


# parametrising the test below because I will add more cases
@pytest.mark.parametrize("simplified,n_words", [("是", 140)])
def test_get_simplified_word_containing_char(
    db: Session, simplified: str, n_words: int
):
    word_results: List[Row] = get_simplified_word_containing_char(
        db, simplified=simplified
    )
    assert len(word_results) == n_words


@pytest.mark.parametrize(
    "simplified,traditional,pinyin_accent,definitions,classifiers,frequency,n_words",
    [
        (
            "我们",
            "我們",
            "wǒ men",
            "we; us; ourselves; our",
            "",
            283794,
            1,
        ),
        (
            "越来越",
            "越來越",
            "yuè lái yuè",
            "more and more",
            "",
            13386,
            1,
        ),
        (
            "不好意思",
            "不好意思",
            "bù hǎo yì si",
            "to feel embarrassed; to find it embarrassing; to be sorry (for inconveniencing sb)",
            "",
            3667,
            1,
        ),
        (
            "简直",
            "簡直",
            "jiǎn zhí",
            "simply; at all; practically",
            "",
            6776,
            1,
        ),
        (
            "风景",
            "風景",
            "fēng jǐng",
            "scenery; landscape",
            "个",
            3572,
            1,
        ),
        (
            "人",
            "人",
            "rén",
            "man; person; people",
            "个; 位",
            373857,
            1,
        ),
        (
            "一掬同情之泪",
            "一掬同情之淚",
            "yī jū tóng qíng zhī lèi",
            "to shed tears of sympathy (idiom)",
            "",
            6639327,
            1,
        ),
        (
            "3C",
            "3C",
            "sān C",
            "abbr. for computers, communications, and consumer electronics; China Compulsory Certificate (CCC)",
            "",
            6639327,
            1,
        ),
        (
            "USB记忆棒",
            "USB記憶棒",
            "U S B jì yì bàng",
            "USB flash drive; see also 闪存盘(shǎn cún pán)",
            "",
            6639327,
            1,
        ),
        (
            "一哄而散",
            "一哄而散",
            "yī hōng ér sàn",
            "to disperse in confusion (idiom)",
            "",
            6639327,
            2,
        ),
        (
            "不畏强权",
            "不畏強權",
            "bù wèi qiáng quán",
            "not to submit to force (idiom); to defy threats and violence",
            "",
            6639327,
            1,
        ),
    ],
)
def test_simplified_words(
    db: Session,
    simplified: str,
    traditional: str,
    pinyin_accent: str,
    definitions: str,
    classifiers: str,
    frequency: int,
    n_words: int,
):
    word_results: List[Row] = get_simplified_word(db, simplified=simplified)
    assert len(word_results) == n_words
    word: Word = word_results[0].Word
    assert isinstance(word, Word)
    assert word.simplified == simplified
    assert word.traditional == traditional
    assert word.pinyin_accent == pinyin_accent
    assert word.definitions == definitions
    assert word.classifiers == classifiers
    assert word.frequency == frequency
