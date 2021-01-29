from sqlalchemy import Column, Integer, String
from db import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(50))
    traditional = Column(String(50))
    pinyin_num = Column(String(100))
    pinyin_accent = Column(String(100))
    pinyin_clean = Column(String(100))
    pinyin_no_spaces = Column(String(100))
    definitions = Column(String(500))

    def __repr__(self):
        return f"<Word(simplified='{self.simplified}', pinyin='{self.pinyin_accent}'"

