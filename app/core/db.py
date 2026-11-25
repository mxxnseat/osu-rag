from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from app.configs.database import DatabaseSettingsDep

@lru_cache
def create_cached_engine(db_url: str):
    return create_engine(db_url)

def get_engine(settings: DatabaseSettingsDep) -> Engine:
    return create_cached_engine(settings.database_url)

def get_session(engine: Annotated[Engine, Depends(get_engine)]):
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
