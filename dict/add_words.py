from db import Word
from pinyin_utils import convert_pinyin
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import re
from typing import Tuple, List, Dict, Pattern, Match


FREQ_FILE = "files/internet-zh.num"
CEDICT_FILE = "files/cedict_1_0_ts_utf-8_mdbg.txt"



def parse_line(text_line: str, db_session: Session, freq_dict: Dict[str, float]):
    """
    This function updates the python dictionary and the database
    as each line is read from the CEDICT file.
    What things can be present in a line? Traditional, simplified, numbered pinyin
    and definitions. But in the definitions we can also have "also written as",
    "also pronounced as", "classifiers". Finally, we will also use the freq_dict
    to sort the database by frequency.
    """

    traditional: str = text_line.split(" ")[0]
    simplified: str = text_line.split(" ")[1]
    pinyin: str = text_line[text_line.find("[") + 1 : text_line.find("]")]
    # ok first thing is to convert numbered pinyin to accent, clean and no_spaces
    pinyin_accent: str
    pinyin_clean: str
    try:
        pinyin_accent = " ".join(convert_pinyin(pinyin.split(), "accent"))
        pinyin_clean = " ".join(convert_pinyin(pinyin.split(), "clean"))
    except TypeError:
        pinyin_accent = ""
        pinyin_clean = ""
    pinyin_no_spaces: str = pinyin_clean.replace(" ", "")
    # then everything else is part of definitions
    # now let's focus on the definitions part
    # let's convert the numbered pinyin in definitions to accent pinyin
    # (traditional) Chinese medicine/CL:服[fu4],種|种[zhong3]
    # doctor/CL:個|个[ge4],位[wei4],名[ming2]"  -> "doctor/CL:個|个 gè,位 wèi,名 míng
    # note that any pinyin is in square brackets
    # so let's match some square brackets in there
    unparsed_definitions: str = text_line[text_line.find("/")+1 : text_line.rfind("/")]
    # let's first convert any pinyin present within definitions
    pattern: Pattern = re.compile('\[[\w ]+\]')
    for match in pattern.findall(unparsed_definitions):
        numbered_pinyin: str = match[1:-1]
        accent_pinyin: str = " ".join(convert_pinyin(numbered_pinyin.split(), "accent"))
        unparsed_definitions = unparsed_definitions.replace(match, "("+accent_pinyin+")")
    # ok now let's deal with CL, i.e. classifiers/measure words and/or
    # also pronounced as, and/or also written as, etc.
    # they are separated from definitions with a / as well
    unparsed_defs_list: List[str] = unparsed_definitions.split("/")
    # we can have the following things in there
    english_defs_list: List[str] = []
    classifiers_list: List[str] = []
    also_written: str = ""
    also_pronounced: str = ""
    # all of them with have english_def, but only some will have the rest
    # let's write a few regular expressions to match them
    classifier_pattern: Pattern = re.compile('CL:') # this one's easy
    also_written_pattern: Pattern = re.compile('^also written ')
    # for character pair pattern, I used the Unicode range for Chinese characters
    # the common ones (21 something thousand)
    character_pair_pattern: Pattern = re.compile("([\\u4e00-\\u9fa5]+\\|[\\u4e00-\\u9fa5]+)|([\\u4e00-\\u9fa5]+)")
    also_pronounced_pattern: Pattern = re.compile("^also pr. ")

    # now let's extract any classifiers from unparsed_defs_list
    for substring in unparsed_defs_list:
        # does it match a classifier pattern?
        classifier_match: Match = classifier_pattern.search(substring)
        also_written_match: Match = also_written_pattern.search(substring)
        also_pronounced_match: Match = also_pronounced_pattern.search(substring)
        if classifier_match:
            classifier_matches: List[str] = character_pair_pattern.findall(substring)
            # might get a list like [('', '服'), ('種|种', '')]
            # or like [('', '瓶'), ('', '杯'), ('', '罐'), ('', '盒')]
            # if there's a pair, like in 種|种, get the simplified one
            # if the program settings choose traditional, the traditional
            # version will be extracted from the database 
            classifiers_list.extend([max(i)[-1] for i in classifier_matches])
        # does it match a also_written as?
        elif also_written_match:
            # extract the characters from the substring
            # it could be one version of characters like 霍金
            # or could be something like traditional|simplified
            # also written 鐳射|镭射
            # either way, get the simplified one
            also_written = substring.split("|")[-1]
        # check if it also matches a also pronounced
        elif also_pronounced_match:
            # extract the pinyin (already has accent)
            also_pronounced = substring[also_pronounced_match.end():]
            also_pronounced = also_pronounced.replace("[", "")
            also_pronounced = also_pronounced.replace("]", "")
            also_pronounced = also_pronounced.replace("(", "")
            also_pronounced = also_pronounced.replace(")", "")
        else:
            # will be the english definitions
            english_defs_list.append(substring)
    # finally nothing more to extract
    # in the definitions we could have pairs of traditional/simplified
    # characters. Let's only leave the simplified one
    definitions: str = "; ".join(definition for definition in english_defs_list)
    classifiers: str = "; ".join(classifier for classifier in classifiers_list)
    character_pair_list: List[Tuple[str]] = character_pair_pattern.findall(definitions)
    if len(character_pair_list) > 0:
        for pair in character_pair_list:
            to_be_replaced: str = max(pair)
            to_replace_with: str = to_be_replaced.split("|")[-1]
            definitions = definitions.replace(to_be_replaced, to_replace_with)
    # sike, there's still the frequency
    freq: float = int(max(freq_dict.values())*100) + 9999
    try:
        freq = int(freq_dict[simplified]*100)
    except KeyError:
        pass


    # add the data to the database
    db_session.add(
        Word(
            simplified=simplified,
            traditional=traditional,
            pinyin_num=pinyin,
            pinyin_accent=pinyin_accent,
            pinyin_clean=pinyin_clean,
            pinyin_no_spaces=pinyin_no_spaces,
            definitions=definitions,
            also_written=also_written,
            also_pronounced=also_pronounced,
            classifiers=classifiers,
            frequency=freq
        )
    )



if __name__ == "__main__":
    engine = create_engine("sqlite:///dictionary.db", future=True)
    Session = sessionmaker(bind=engine, future=True)
    db_session: Session = Session()

    # let's open the frequency file and create a dictionary
    with open(FREQ_FILE, "r", encoding="utf-8") as freq_file:
        freq_dict: Dict[str, float] = {
            line.split(" ")[2].rstrip(): float(line.split(" ")[1])
            for line in freq_file.read().splitlines()[4:]
        }

    with open(CEDICT_FILE, "r", encoding="utf-8") as dict_file:
        for line in dict_file:
            parse_line(line, db_session, freq_dict)
        db_session.commit()
        db_session.close()
        engine.dispose()