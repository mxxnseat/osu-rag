from app.core.errors import DuplicateKeyError, DatabaseError
from app.core.db import SessionDep
from typing import ClassVar, Generic, TypeVar

from psycopg import errors
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

TEntity = TypeVar("TEntity")
TPayload = TypeVar("TPayload", bound=BaseModel)

class Repository[TEntity]():
    entity: ClassVar[type]  # set in child class

    def __init__(self, session: SessionDep):
        self.session = session

    def create_(self, payload: BaseModel) -> TEntity | DatabaseError:
        obj = self.entity(**payload.model_dump())
        self.session.add(obj)
        self.session.commit()
        return obj

    def executor(self, fn):
        try:
            return fn()
        except IntegrityError as e:
            if isinstance(e.orig, errors.UniqueViolation):
                return DuplicateKeyError()
            return DatabaseError(e._message())
        except SQLAlchemyError as e:
            return DatabaseError(e._message())
        finally:
            self.session.rollback()