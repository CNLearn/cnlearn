from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


SQLALCHEMY_DATABASE = "sqlite+pysqlite:///db/dictionary.db"
#SQLALCHEMY_DATABASE = "sqlite+pysqlite:////workspaces/gui_cnlearn/src/db/dictionary.db"
engine = create_engine(
    SQLALCHEMY_DATABASE, echo=False, future=True
    #, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
session: Session = SessionLocal()