import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'dictionary.db')
SQLALCHEMY_DATABASE = "sqlite+pysqlite:////{db}".format(db=db)
engine = create_engine(
    SQLALCHEMY_DATABASE, echo=False, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)