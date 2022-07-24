from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .schemas import settings

DB_URL = settings.SQLALCHEMY_DATABASE_URI

if "sqlite" in DB_URL:
    DB_URL = DB_URL + "?check_same_thread=False"

engine = create_engine(DB_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
