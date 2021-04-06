"""
This script is run in order to create the character search
database. It creates a SQLite database through SQLAlchemy.
"""


# used for type hints
from typing import Any, Tuple, List, Dict, Pattern, Match, Union
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from json import loads

# for database stuff
from db import Word, Character

# for matching
import re


# define the file where the CEDICT is stored
CHARACTER_FILE = "files/character_data.txt"
FREQ_FILE = "files/internet-zh.num"


def parse_line(text_line: str, db_session: Session, freq_dict: Dict[str, float]):
    """
    This function updates the Characters table in the database using the
    character data file. The data file has several (some optional) fields for
    each character:
        - character (unique, I think)
        - definition (optional, some have it, some don't)
        - pinyin (comma separated list of pronounciations,
                  might be an empty list)
        - decomposition (ideograph description sequence, can contain ? if
                        parts of it are unknown)
        - etymology (etymology of the character, might be null)
        - radical - will be present
        - matches - map strokes to the strokes of its components (can be null)
    """
    # fields: List[str] = [
    #     "character",
    #     "definition",
    #     "pinyin",
    #     "decomposition",
    #     "etymology",
    #     "radical",
    #     "matches",
    # ]

    character_dictionary: Dict[str, Any] = loads(text_line)
    # now it's a dictionary
    # let's save the various things to variables
    character: str = character_dictionary["character"]
    # the definition may or may not be present
    try:
        definition: str = character_dictionary["definition"]
    except KeyError:
        definition = None
    # pinyin
    pinyin: str = "; ".join(i for i in character_dictionary["pinyin"])
    # decomposition. Invalid if it starts with ?
    if character_dictionary["decomposition"][0] == "？":
        decomposition = None
    else:
        decomposition: str = character_dictionary["decomposition"]
    # etymology, may or not be present
    try:
        etymology: Dict = character_dictionary["etymology"]
    except KeyError:
        etymology = None
    # radical, required
    radical: str = character_dictionary["radical"]
    # matches
    matches: str = str(character_dictionary["matches"])
    # add the frequency
    freq: float = int(max(freq_dict.values()) * 100) + 9999
    try:
        freq = int(freq_dict[character] * 100)
    except KeyError:
        pass


    # add the data to the database
    db_session.add(
        Character(
            character=character,
            definition=definition,
            pinyin=pinyin,
            decomposition=decomposition,
            etymology=etymology,
            radical=radical,
            matches=matches,
            frequency=freq,
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

    with open(CHARACTER_FILE, "r", encoding="utf-8") as f:

        for line in f:
            parse_line(line, db_session, freq_dict)

        # commit the changes to the databaes
        db_session.commit()
        # # close the connection
        db_session.close()
        engine.dispose()
