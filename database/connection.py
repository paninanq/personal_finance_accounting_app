from functools import lru_cache

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from setting import DB_FULL_URL


@lru_cache
def get_db_sessionmaker() -> sessionmaker:
    return sessionmaker(
        create_engine(DB_FULL_URL),
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
