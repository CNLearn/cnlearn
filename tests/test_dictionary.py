from typing import Dict, List
from cnlearn.search.dictionary import Dictionary
from cnlearn.schemas.structures import Character, Word
from cnlearn.db.models import Word as Word_model, Character as Character_model
import pytest


@pytest.fixture
def dictionary() -> Dictionary:
    """
    Returns a reusable database session.
    """
    d = Dictionary()
    return d


@pytest.fixture
def hao_characters() -> List[Character]:
    hao_1 = Character(
        id=27949,
        definitions="good; well; proper; good to; easy to; very; so; (suffix indicating completion or readiness); (of two people) close; on intimate terms; (after a personal pronoun) hello",
        stroke_diagram=None,
        simplified="好",
        traditional="好",
        pinyin_num="hao3",
        pinyin_accent="hǎo",
        pinyin_clean="hao",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=165789,
        character_type=None,
        radical="女",
        decomposition="⿰女子",
        etymology={"type": "ideographic", "hint": "A woman\xa0女 with a son\xa0子"},
    )
    hao_2 = Character(
        id=27950,
        definitions="to be fond of; to have a tendency to; to be prone to",
        stroke_diagram=None,
        simplified="好",
        traditional="好",
        pinyin_num="hao4",
        pinyin_accent="hào",
        pinyin_clean="hao",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=165789,
        character_type=None,
        radical="女",
        decomposition="⿰女子",
        etymology={"type": "ideographic", "hint": "A woman\xa0女 with a son\xa0子"},
    )
    return [hao_1, hao_2]


@pytest.fixture
def buhaoyisi_word() -> Word:
    """
    Returns the Word structure and Character components for 不好意思.
    """
    bu: Character = Character(
        id=1846,
        definitions="(negative prefix); not; no",
        stroke_diagram=None,
        simplified="不",
        traditional="不",
        pinyin_num="bu4",
        pinyin_accent="bù",
        pinyin_clean="bu",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=459467,
        character_type=None,
        radical="一",
        decomposition="⿱一？",
        etymology={"type": "ideographic", "hint": "A bird flying toward the sky\xa0一"},
    )
    hao: Character = Character(
        id=27949,
        definitions="good; well; proper; good to; easy to; very; so; (suffix indicating completion or readiness); (of two people) close; on intimate terms; (after a personal pronoun) hello",
        stroke_diagram=None,
        simplified="好",
        traditional="好",
        pinyin_num="hao3",
        pinyin_accent="hǎo",
        pinyin_clean="hao",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=165789,
        character_type=None,
        radical="女",
        decomposition="⿰女子",
        etymology={"type": "ideographic", "hint": "A woman\xa0女 with a son\xa0子"},
    )
    yi: Character = Character(
        id=39615,
        definitions="idea; meaning; thought; to think; wish; desire; intention; to expect; to anticipate",
        stroke_diagram=None,
        simplified="意",
        traditional="意",
        pinyin_num="yi4",
        pinyin_accent="yì",
        pinyin_clean="yi",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=8201,
        character_type=None,
        radical="心",
        decomposition="⿱音心",
        etymology={
            "type": "pictophonetic",
            "phonetic": "音",
            "semantic": "心",
            "hint": "heart",
        },
    )
    si: Character = Character(
        id=38511,
        definitions="to think; to consider",
        stroke_diagram=None,
        simplified="思",
        traditional="思",
        pinyin_num="si1",
        pinyin_accent="sī",
        pinyin_clean="si",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=6943,
        character_type=None,
        radical="心",
        decomposition="⿱田心",
        etymology={
            "type": "ideographic",
            "hint": "Weighing something with your mind\xa0囟 (altered) and heart\xa0心",
        },
    )
    buhaoyisi: Word = Word(
        id=2117,
        definitions="to feel embarrassed; to find it embarrassing; to be sorry (for inconveniencing sb)",
        stroke_diagram=None,
        simplified="不好意思",
        traditional="不好意思",
        pinyin_num="bu4 hao3 yi4 si5",
        pinyin_accent="bù hǎo yì si",
        pinyin_clean="bu hao yi si",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=3667,
        pinyin_no_spaces="buhaoyisi",
        components=[bu, hao, yi, si],
        radical=None,
        hsk=None,
    )
    return buhaoyisi


@pytest.fixture
def yidali_word() -> Word:
    return Word(
        id=39630,
        definitions="Italy; Italian",
        stroke_diagram=None,
        simplified="意大利",
        traditional="意大利",
        pinyin_num="Yi4 da4 li4",
        pinyin_accent="Yì dà lì",
        pinyin_clean="Yi da li",
        also_pronounced="",
        also_written="",
        classifiers="",
        frequency=4049,
        pinyin_no_spaces="Yidali",
        components=[
            Character(
                id=39614,
                definitions="Italy; Italian; abbr. for 意大利(Yì dà lì)",
                stroke_diagram=None,
                simplified="意",
                traditional="意",
                pinyin_num="Yi4",
                pinyin_accent="Yì",
                pinyin_clean="Yi",
                also_pronounced="",
                also_written="",
                classifiers="",
                frequency=8201,
                character_type=None,
                radical="心",
                decomposition="⿱音心",
                etymology={
                    "type": "pictophonetic",
                    "phonetic": "音",
                    "semantic": "心",
                    "hint": "heart",
                },
            ),
            Character(
                id=25709,
                definitions="big; huge; large; major; great; wide; deep; older (than); oldest; eldest; greatly; very much; (dialect) father; father's elder or younger brother",
                stroke_diagram=None,
                simplified="大",
                traditional="大",
                pinyin_num="da4",
                pinyin_accent="dà",
                pinyin_clean="da",
                also_pronounced="",
                also_written="",
                classifiers="",
                frequency=176304,
                character_type=None,
                radical="大",
                decomposition="⿻一人",
                etymology={
                    "type": "ideographic",
                    "hint": "A man\xa0人 with outstretched arms",
                },
            ),
            Character(
                id=12976,
                definitions="sharp; favorable; advantage; benefit; profit; interest; to do good to; to benefit",
                stroke_diagram=None,
                simplified="利",
                traditional="利",
                pinyin_num="li4",
                pinyin_accent="lì",
                pinyin_clean="li",
                also_pronounced="",
                also_written="",
                classifiers="",
                frequency=11305,
                character_type=None,
                radical="刂",
                decomposition="⿰禾刂",
                etymology={
                    "type": "ideographic",
                    "hint": "Harvesting\xa0刂\xa0grain\xa0禾",
                },
            ),
        ],
        radical=None,
        hsk=None,
    )


def test_dict_is_created(dictionary: Dictionary):
    """
    Checks if the dictionary object was created and is usable.
    """
    assert dictionary.search_term == ""
    assert len(dictionary.dictionary_cache) == 0
    assert len(dictionary.unknown_words) == 0
    assert len(dictionary.words_found) == 0
    assert len(dictionary.search_history) == 0


def test_one_character_multiple_results(dictionary, hao_characters):
    """
    Checks the results for when `好` is searched for.
    """
    dictionary.search_chinese("好")
    assert dictionary.search_term == "好"
    assert len(dictionary.words_found) == 2
    assert "好" in dictionary.dictionary_cache
    assert len(dictionary.dictionary_cache) == 1
    assert len(dictionary.dictionary_cache["好"]) == 2
    assert all(character in dictionary.words_found for character in hao_characters)
    assert all(
        character in dictionary.dictionary_cache["好"] for character in hao_characters
    )


def test_dictionary_reuse(dictionary, mocker):
    """
    in order to see the cache work, let's mock the crud functions and
    see how many times they are called.
    """
    hao_word_1 = Word_model(
        traditional="好",
        pinyin_accent="hǎo",
        id=27949,
        pinyin_no_spaces="hao",
        also_pronounced="",
        definitions="good; well; proper; good to; easy to; very; so; (suffix indicating completion or readiness); (of two people) close; on intimate terms; (after a personal pronoun) hello",
        frequency=165789,
        pinyin_num="hao3",
        simplified="好",
        pinyin_clean="hao",
        also_written="",
        classifiers="",
    )
    hao_word_2 = Word_model(
        traditional="好",
        pinyin_accent="hào",
        id=27950,
        pinyin_no_spaces="hao",
        also_pronounced="",
        definitions="to be fond of; to have a tendency to; to be prone to",
        frequency=165789,
        pinyin_num="hao4",
        simplified="好",
        pinyin_clean="hao",
        also_written="",
        classifiers="",
    )
    hao_character = Character_model(
        character="好",
        pinyin="hǎo",
        etymology={"type": "ideographic", "hint": "A woman\xa0女 with a son\xa0子"},
        matches="[[0], [0], [0], [1], [1], [1]]",
        definition="good, excellent, fine; proper, suitable; well",
        decomposition="⿰女子",
        id=1595,
        radical="女",
        frequency=165789,
    )
    mocked_get_word_and_character = mocker.patch(
        # the function to mock is imported in the dictionary class file
        "cnlearn.search.dictionary.get_word_and_character",
        return_value=[
            (hao_word_1, hao_character),
            (hao_word_2, hao_character),
        ],
    )
    dictionary.search_chinese("好")
    assert mocked_get_word_and_character.call_count == 1

    # let's do the same search again. this time, the dictionary object
    # should get it from cache
    dictionary.search_chinese("好")
    assert mocked_get_word_and_character.call_count == 1

    # ok maybe you don't believe me? Let's look for another word
    # please note that the return won't be the correct one for
    # 我, rather it will be the same as it was for 好
    # but that's fine, I'm testing how many times the function
    # gets called and if the cache works
    dictionary.search_chinese("我")
    assert mocked_get_word_and_character.call_count == 2
    # now do you believe me?
    dictionary.search_chinese("好")
    assert mocked_get_word_and_character.call_count == 2
    # and now??? I can keep going...
    dictionary.search_chinese("好")
    assert mocked_get_word_and_character.call_count == 2
    # ok that's enough for this test.


def test_multiple_character_word(dictionary, buhaoyisi_word):
    """
    This will test a multiple character word that will find the word
    and have 4 component characters.
    """
    dictionary.search_chinese("不好意思")
    assert buhaoyisi_word in dictionary.words_found


def test_multiple_character_word_2(dictionary, yidali_word):
    """
    This will test a multiple character word with a specific 
    pinyin that is found in the database.
    """
    dictionary.search_chinese("意大利")
    assert yidali_word in dictionary.words_found
