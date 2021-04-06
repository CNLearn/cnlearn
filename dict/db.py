from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import registry
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import create_engine

mapper_registry = registry()


@mapper_registry.mapped
class Word:
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(50))
    traditional = Column(String(50))
    pinyin_num = Column(String(100))
    pinyin_accent = Column(String(100))
    pinyin_clean = Column(String(100))
    pinyin_no_spaces = Column(String(100))
    also_written = Column(String(100))
    also_pronounced = Column(String(100))
    classifiers = Column(String(100))
    definitions = Column(String(500))
    frequency = Column(Integer)

    def __repr__(self):
        return f"<Word(simplified='{self.simplified}', pinyin='{self.pinyin_accent}>'"


@mapper_registry.mapped
class Character:
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    character = Column(String(1))
    definition = Column(String(150), nullable=True)
    pinyin = Column(String(50))
    decomposition = Column(String(15))
    etymology = Column(JSON(), nullable=True)
    radical = Column(String(1))
    matches = Column(String(100))
    frequency = Column(Integer)

    def __repr__(self):
        return f"<Character({self.character}, radical='{self.radical})>"

engine = create_engine("sqlite:///dictionary.db")
with engine.begin() as connection:
    mapper_registry.metadata.create_all(connection)

