from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE = "sqlite+pysqlite:///db/dictionary.db"
engine = create_engine(
    SQLALCHEMY_DATABASE, echo=False, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)