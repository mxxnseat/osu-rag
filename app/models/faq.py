from pgvector.sqlalchemy import Vector
from sqlmodel import Column, SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB

class Faq(SQLModel, table=True):
    __tablename__ = "faqs"
    
    id: int | None = Field(default=None, primary_key=True)
    title: str
    section: str
    content: str
    embedding: list[float] = Field(sa_column=Column(Vector(384)))
    chunk_index: int
