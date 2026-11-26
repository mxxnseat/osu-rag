from pydantic import BaseModel
from app.dtos.base import BaseBody, SearchOptions, BaseResponse

# Services
class AddFaqBody(BaseBody):
    content: str
    title: str
    section: str
    path: list[str]
    chunk_index: int
    
class FaqResponse(BaseResponse):
    content: str

class FaqSearchPayload(BaseModel):
    question: str

# Repositories
class RFaqSearchPayload(BaseModel):
    question: list[float]
    min_confidence: float

class RFaqSearchOptions(SearchOptions):
    ...

class RCreateFaqPayload(BaseBody):
    model_config = {"extra": "ignore"}

    title: str
    section: str
    content: str
    embedding: list[float]
    chunk_index: int
    hash: str