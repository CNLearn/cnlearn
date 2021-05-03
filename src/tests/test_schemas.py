import pytest
from sqlalchemy.orm.session import Session
from src.schemas.structures import Character, Word
from src.db.models import Word as Word_model, Character as Character_model
from src.db.crud import (
    get_simplified_word,
    get_word_and_character,
)
from src.db.settings import SessionLocal


@pytest.fixture
def db() -> Session:
    """
    Returns a reusable database session.
    """
    session: Session = SessionLocal()
    return session


@pytest.fixture
def my_character_1() -> Character:
    return Character(
        simplified="不",
        traditional="不",
        pinyin_num="bu4",
        pinyin_accent="bù",
        pinyin_clean="bu",
        definitions="(negative prefix); not; no",
        decomposition="⿱一？",
        etymology={
            "type": "ideographic",
            "hint": "A bird flying toward the sky\u00a0\u4e00",
        },
        radical="一",
        frequency=459467,
    )


@pytest.fixture
def my_character_2() -> Character:
    return Character(
        simplified="满",
        traditional="滿",
        definitions="to fill; full; filled; packed; fully; completely; quite; to reach the limit; to satisfy; satisfied; contented",
        pinyin_num="man3",
        pinyin_accent="mǎn",
        pinyin_clean="man",
        decomposition="⿰氵⿱艹两",
        etymology={
            "type": "pictophonetic",
            "phonetic": "\u34bc",
            "semantic": "\u6c35",
            "hint": "water",
        },
        radical="氵",
        frequency=10702,
    )


@pytest.fixture
def my_word_1(my_character_1, my_character_2) -> Word:
    return Word(
        simplified="不满",
        traditional="不滿",
        definitions="resentful; discontented; dissatisfied",
        pinyin_num="bu4 man3",
        pinyin_accent="bù mǎn",
        pinyin_clean="bu man",
        pinyin_no_spaces="buman",
        # for now I am manually specifying what the components are
        # later they will be created automatically
        components=[my_character_1, my_character_2],
        frequency="3157",
    )


# let's test some of the dictionaries created


def test_character1_dictionary(my_character_1: Character):
    """
    Tests the fields from Character 1.
    """
    character: Character = my_character_1
    assert character.definitions == "(negative prefix); not; no"
    assert character.simplified == character.traditional == "不"
    assert character.pinyin_accent == "bù"
    assert character.pinyin_num == "bu4"
    assert character.pinyin_clean == "bu"


def test_word_1_components(
    my_word_1: Word, my_character_1: Character, my_character_2: Character
):
    """
    Tests the component characters of a Word schema.
    """
    word: Word = my_word_1
    assert my_character_1 in word.components and my_character_2 in word.components


def test_bu_character_database(db, my_character_1):
    """
    Tests the results for the 不 character from the database through the Character schema
    """
    bu_word, bu_character = get_word_and_character(db, simplified="不")
    bu_character_schema: Character = Character.from_orm(bu_word)
    bu_character_schema.decomposition = bu_character.decomposition
    bu_character_schema.etymology = bu_character.etymology
    bu_character_schema.radical = bu_character.radical
    assert bu_character_schema.traditional == my_character_1.traditional
    assert bu_character_schema.simplified == my_character_1.simplified
    assert bu_character_schema.pinyin_num == my_character_1.pinyin_num
    assert bu_character_schema.pinyin_accent == my_character_1.pinyin_accent
    assert bu_character_schema.pinyin_clean == my_character_1.pinyin_clean
    assert bu_character_schema.definitions == my_character_1.definitions
    assert bu_character_schema.decomposition == my_character_1.decomposition
    assert bu_character_schema.etymology == my_character_1.etymology
    assert bu_character_schema.radical == my_character_1.radical


def test_man_character_database(db, my_character_2):
    """
    Tests the results for the 满 character from the database through the Character schema
    """
    man_word, man_character = get_word_and_character(
        db, simplified="满", pinyin_clean="man"
    )
    man_character_schema: Character = Character.from_orm(man_word)
    man_character_schema.decomposition = man_character.decomposition
    man_character_schema.etymology = man_character.etymology
    man_character_schema.radical = man_character.radical
    assert man_character_schema.traditional == my_character_2.traditional
    assert man_character_schema.simplified == my_character_2.simplified
    assert man_character_schema.pinyin_num == my_character_2.pinyin_num
    assert man_character_schema.pinyin_accent == my_character_2.pinyin_accent
    assert man_character_schema.pinyin_clean == my_character_2.pinyin_clean
    assert man_character_schema.definitions == my_character_2.definitions
    assert man_character_schema.decomposition == my_character_2.decomposition
    assert man_character_schema.etymology == my_character_2.etymology
    assert man_character_schema.radical == my_character_2.radical


def test_buman_character_database(db, my_word_1):
    """
    Tests the results for the 不满 word from the database through the Word schema
    """
    bu_man_word_list: Word_model = get_simplified_word(db, simplified="不满")
    bu_man_word_schema = Word.from_orm(bu_man_word_list[0].Word)
    assert bu_man_word_schema.traditional == my_word_1.traditional
    assert bu_man_word_schema.simplified == my_word_1.simplified
    assert bu_man_word_schema.pinyin_num == my_word_1.pinyin_num
    assert bu_man_word_schema.pinyin_accent == my_word_1.pinyin_accent
    assert bu_man_word_schema.pinyin_clean == my_word_1.pinyin_clean
    assert bu_man_word_schema.definitions == my_word_1.definitions