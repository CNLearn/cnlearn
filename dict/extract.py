"""
This script is run in order to create the word search
database. It creates a JSON format one, a SQLite database
through SQLAlchemy.
Other formats might be explored in the future if they
improve performance.
"""

# used for saving the dictionary to json format
import io
import json
# used to create a python dictionary that can have duplicate keys
from collections import defaultdict

# used for type hints
from typing import Union, List, DefaultDict, Dict

# for database stuff
from db import SessionLocal, engine
import db_models
# from . import db_models




# define the file where the CEDICT is stored
CEDICT_FILE = "cedict/cedict_1_0_ts_utf-8_mdbg.txt"


def convert_to_pinyin_accent(word: str) -> str:
    """
    This function converts a pinyin with numbers to pinyin with accents.
    """
    # the list below is a list of vowels that appear in the CEDICT pinyin
    vowels: List[str] = ["a", "e", "i", "o", "u", "u:", "A", "E", "I", "O", "U", "U:"]
    # the dictionary below will convert the vowels to vowels with accents
    # depening on their tone as specified at the end of the word
    vowel_dict: Dict[int, List[str]] = {
        1: ["ā", "ē", "ī", "ō", "ū", "ǖ", "Ā", "Ē", "Ī", "Ō", "Ū", "Ǖ"],
        2: ["á", "é", "í", "ó", "ú", "ǘ", "Á", "É", "Í", "Ó", "Ú", "Ǘ"],
        3: ["ǎ", "ě", "ǐ", "ǒ", "ǔ", "ǚ", "Ǎ", "Ě", "Ǐ", "Ǒ", "Ǔ", "Ǚ"],
        4: ["à", "è", "ì", "ò", "ù", "ǜ", "À", "È", "Ì", "Ò", "Ù", "Ǜ"],
        5: ["a", "e", "i", "o", "u", "ü", "A", "E", "I", "O", "U", "Ü"],
    }
    tone: int = ord(word[-1]) - 48
    pos: Union[int, None]
    pinyin_word: str
    if 0 < tone < 6:
        word_without_tone = word[0:-1]
        if tone < 5:
            # the following vowels/pairs always get the marker
            search_list: List[str] = ["a", "e", "ou"]
            # check if the word_without_tone has any of them
            found: List[bool] = [vowel in word_without_tone for vowel in search_list]
            if any(found):
                vowel: int = search_list[found.index(True)]
                pos = word_without_tone.find(vowel)
            else:
                pos = last_vowel(word_without_tone)

            # now we need to check whether the vowel position is
            # followed by : since we would have to consider two letters
            if pos is not None:
                try:
                    if word_without_tone[pos + 1] == ":":
                        to_replace: str = word_without_tone[pos : pos + 2]
                    else:
                        to_replace: str = word_without_tone[pos : pos + 1]
                except IndexError:
                    to_replace: str = word_without_tone[pos : pos + 1]
                pinyin_word = word_without_tone.replace(
                    to_replace, vowel_dict[tone][vowels.index(to_replace)]
                )
            else:
                pinyin_word = word_without_tone
        else:
            pinyin_word = word_without_tone.replace("u:", "ü")
            pinyin_word = word_without_tone.replace("U:", "Ü")
    else:
        pinyin_word = word
    return pinyin_word


def convert_to_pinyin_clean(word: str) -> str:
    """
    This functions converts from pinyin with numbers to pinyin
    without numbers or accents.
    """
    tone: int = ord(word[-1]) - 48
    pinyin_clean: str
    if 0 < tone < 6:
        pinyin_clean = word[0:-1]
    else:
        pinyin_clean = word
    return pinyin_clean


def last_vowel(word: str) -> Union[int, None]:
    """
    This function returns the position of the last vowel in a word.
    """
    # another way to reverse a string is ''.join(list(reversed(word)))
    vowels: List[str] = ["a", "e", "i", "o", "u", "u:", "A", "E", "I", "O", "U", "U:"]
    reverse_word: str = word[::-1]
    for character in reverse_word:
        for vowel in vowels:
            if vowel in character:
                return word.find(vowel)
    return None


def convert_pinyin(
    item: Union[str, List[str]], flag: str
) -> Union[str, List[str], None]:
    """
    This function converts pinyin with numbers to either pinyin with tone marks
    (accents) or clean pinyin (no numbers or accents).
    """
    if flag in ("accent", "clean"):
        if isinstance(item, str):
            if flag == "accent":
                return convert_to_pinyin_accent(item)
            # flag is clean
            return convert_to_pinyin_clean(item)
        if isinstance(item, list):
            pinyin_list = []
            for i in item:
                pinyin_list.append(convert_pinyin(i, flag))
            return pinyin_list
        raise ValueError("Text must be a string or list of strings.")
    raise ValueError("Flag must be `accent` or `clean`.")


# Instead of using a Python dictionary, let's now use a defaultdict that can
# store multiple values in a list for a key. Why do I need to do that? Well,
# I made silly mistake. One of the harder things about learning Chinese are
# characters that have multiple pronunciations. They are written the same
# but pronounced differently. So what my original script did was everytime
# it processed a line, if there was a character it had already seen before, it
# would then replace the information for it with the one it had just seen.
# We want to be able to access all the meanings, so am using a defaultdict now.


def parse_line(text_line, json_dictionary, db_session):
    """
    This function updates the python dictionary and the database
    as each line is read from the CEDICT file.
    """
    traditional = text_line.split(" ")[0]
    simplified = text_line.split(" ")[1]
    pinyin = text_line[text_line.find("[") + 1 : text_line.find("]")]
    definitions = "; ".join(
        text_line[text_line.find("/") + 1 : text_line.rfind("/")].split("/")
    )
    try:
        pinyin_accent = " ".join(convert_pinyin(pinyin.split(), "accent"))
        pinyin_clean = " ".join(convert_pinyin(pinyin.split(), "clean"))
    except TypeError:
        pinyin_accent = ""
        pinyin_clean = ""
    pinyin_no_spaces = pinyin_clean.replace(" ", "")

    json_dictionary[simplified].append(
        {
            "simplified": simplified,
            "traditional": traditional,
            "pinyin_num": pinyin,
            "pinyin_accent": pinyin_accent,
            "pinyin_clean": pinyin_clean,
            "pinyin_no_spaces": pinyin_no_spaces,
            "definition": definitions,
        }
    )
    # add the same data to the database
    db_session.add(
        db_models.Word(
            simplified = simplified,
            traditional = traditional,
            pinyin_num = pinyin,
            pinyin_accent = pinyin_accent,
            pinyin_clean = pinyin_clean,
            pinyin_no_spaces = pinyin_no_spaces,
            definitions = definitions
        )
    )


if __name__ == "__main__":
    dictionary: DefaultDict = defaultdict(list)
    db_models.Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()

    with open(CEDICT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parse_line(line, dictionary, db_session)
        # commit the changes to the databaes
        db_session.commit()
        # close the connection
        db_session.close()
        engine.dispose()
        

    with io.open("dict.json", "w", encoding="utf8") as json_file:
        json.dump(dictionary, json_file, ensure_ascii=False)
