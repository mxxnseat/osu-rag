from pgvector.sqlalchemy import Vector
from sqlmodel import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB

class Faq(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question: str
    answer: str
    embedding: list[float] = Field(sa_column=Column(Vector(384)))
    