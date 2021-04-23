from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.engine import ChunkedIteratorResult, Row
from src.db.models import Word, Character
from typing import List


def get_simplified_word(db: Session, simplified: str, pinyin: str = None) -> List[Row]:
    word_selection: Select = (
        select(Word).where(Word.simplified == simplified).order_by(Word.frequency)
    )
    if pinyin:
        word_selection = word_selection.where(Word.pinyin_clean == pinyin)
    result: ChunkedIteratorResult = db.execute(word_selection)
    words: List[Row] = result.all()
    return words

def get_simplified_word_containing_char(db: Session, simplified: str, pinyin: str = None) -> List[Row]:
    word_selection: Select = (
        select(Word).where(Word.simplified.contains(simplified)).order_by(Word.frequency)
    )
    if pinyin:
        word_selection = word_selection.where(Word.pinyin_clean.contains(pinyin))
    result: ChunkedIteratorResult = db.execute(word_selection)
    words: List[Row] = result.all()
    return words


def get_simplified_character(db: Session, simplified: str) -> Row:
    character: Row = db.execute(
        select(Character).where(Character.character == simplified)
    ).first()
    return character


def get_word_and_character(
    db: Session, simplified: str, pinyin_clean: str = None, pinyin_accent: str = None
) -> Row:
    word_and_character_select: Select = (
        select(Word, Character)
        .where(
            and_(
                Word.simplified == simplified,
                Word.simplified == Character.character,
            )
        )
        .order_by(Word.frequency)
    )
    if pinyin_clean:
        word_and_character_select = word_and_character_select.where(
            Word.pinyin_clean == pinyin_clean
        )
    if pinyin_accent:
        word_and_character_select = word_and_character_select.where(
            Word.pinyin_accent == pinyin_accent
        )
    word_and_character: Row = db.execute(word_and_character_select).first()
    return word_and_character
