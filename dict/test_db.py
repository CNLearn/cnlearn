from typing import Dict, Optional

import pytest
from sqlalchemy import select
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .db import Character, Word
from .pinyin_utils import convert_pinyin, last_vowel


@pytest.fixture
def db_session():
    """
    Creates and returns a database session.
    """
    engine = create_engine("sqlite:///dictionary.db", future=True)
    Session = sessionmaker(bind=engine, future=True)
    session: Session = Session()
    return session


@pytest.fixture
def shi_character(db_session: Session):
    """
    This fixture looks for the 是 character in the simplified column of the SQLite
    database. There are two dictionary entries for it. It also looks at all the
    expressions containing 是 in them.
    """
    shi_entries = db_session.execute(select(Word).where(Word.simplified == "是")).all()
    shi_containing_entries = db_session.execute(
        select(Word).where(Word.simplified.contains("是"))
    ).all()
    return (shi_entries, shi_containing_entries)


def test_number_entries_db(db_session: Session):
    """
    This tests counts the number of entries and unique (simplified)
    entries in the CEDICT file.
    """
    # session = db_session
    total_entries: int = len(db_session.execute(select(Word)).all())
    assert total_entries == 116134


def test_number_shi_entries(shi_character):
    """
    This tests the individual 是 entries and the entries containing
    that character.
    """
    individual_shi, group_shi = shi_character
    assert len(individual_shi) == 2
    assert len(group_shi) == 140


def test_individual_shi_entries(shi_character):
    """
    This tests the individual 是 entries.
    """
    individual_shi = shi_character[0]
    shi_1 = individual_shi[0]
    shi_2 = individual_shi[1]
    assert shi_1.Word.traditional == "是"
    assert shi_2.Word.traditional == "昰"
    assert shi_1.Word.pinyin_accent == "shì" and shi_2.Word.pinyin_accent == "shì"
    assert shi_1.Word.definitions == "is; are; am; yes; to be"
    assert shi_2.Word.definitions == "variant of 是(shì); (used in given names)"


@pytest.mark.parametrize(
    "simplified,traditional,pinyin_accent,definitions,classifiers,frequency",
    [
        ("我们", "我們", "wǒ men", "we; us; ourselves; our", "", 283794),
        ("越来越", "越來越", "yuè lái yuè", "more and more", "", 13386),
        (
            "不好意思",
            "不好意思",
            "bù hǎo yì si",
            "to feel embarrassed; to find it embarrassing; to be sorry (for inconveniencing sb)",
            "",
            3667,
        ),
        ("简直", "簡直", "jiǎn zhí", "simply; at all; practically", "", 6776),
        ("风景", "風景", "fēng jǐng", "scenery; landscape", "个", 3572),
        ("人", "人", "rén", "man; person; people", "个; 位", 373857),
        (
            "一掬同情之泪",
            "一掬同情之淚",
            "yī jū tóng qíng zhī lèi",
            "to shed tears of sympathy (idiom)",
            "",
            6639327,
        ),
        (
            "3C",
            "3C",
            "sān C",
            "abbr. for computers, communications, and consumer electronics; China Compulsory Certificate (CCC)",
            "",
            6639327,
        ),
        (
            "USB记忆棒",
            "USB記憶棒",
            "U S B jì yì bàng",
            "USB flash drive; see also 闪存盘(shǎn cún pán)",
            "",
            6639327,
        ),
        (
            "一哄而散",
            "一哄而散",
            "yī hōng ér sàn",
            "to disperse in confusion (idiom)",
            "",
            6639327,
        ),
        (
            "不畏强权",
            "不畏強權",
            "bù wèi qiáng quán",
            "not to submit to force (idiom); to defy threats and violence",
            "",
            6639327,
        ),
    ],
)
def test_words(
    db_session: Session,
    simplified: str,
    traditional: str,
    pinyin_accent: str,
    definitions: str,
    classifiers: str,
    frequency: int,
):
    word = db_session.execute(select(Word).where(Word.simplified == simplified)).first()
    assert word.Word.simplified == simplified
    assert word.Word.traditional == traditional
    assert word.Word.pinyin_accent == pinyin_accent
    assert word.Word.definitions == definitions
    assert word.Word.classifiers == classifiers
    assert word.Word.frequency == frequency


@pytest.mark.parametrize(
    "word,number", [("woah", 2), ("hao", 2), ("kong", 1), ("3 P", None), ("456", None)]
)
def test_last_vowel(word: str, number: Optional[int]):
    """
    Tests the last vowel function.
    """
    assert last_vowel(word) == number


@pytest.mark.xfail(raises=ValueError)
def test_convert_pinyin_exceptions_integer():
    """
    Tests if passing a string or list of strings (such as an integer)
    will raise a ValueError.
    a ValueError.
    """
    convert_pinyin(5, "accent")


@pytest.mark.xfail(raises=ValueError)
def test_convert_pinyin_exceptions_wrong_flag():
    """
    Test if passing a flag not `accent` or `clean` raises a ValueError.
    """
    convert_pinyin(5, "country")


@pytest.mark.parametrize(
    "simplified,pinyin,decomposition,etymology,radical",
    [
        (
            "好",
            "hǎo",
            "⿰女子",
            {
                "type": "ideographic",
                "hint": "A woman 女 with a son 子",
            },
            "女",
        ),
        (
            "戴",
            "dài",
            "⿻⿱十異戈",
            None,
            "戈",
        ),
    ],
)
def test_characters(
    db_session: Session,
    simplified: str,
    pinyin: str,
    decomposition: str,
    etymology: Dict,
    radical: str,
):
    character = db_session.execute(
        select(Character).where(Character.character == simplified)
    ).first()
    assert character.Character.character == simplified
    assert character.Character.pinyin == pinyin
    assert character.Character.decomposition == decomposition
    assert character.Character.etymology == etymology
    assert character.Character.radical == radical
