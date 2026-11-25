from app.dtos.base import BaseBody, SearchOptions, BaseResponse

class AddFaqBody(BaseBody):
    content: str
    title: str
    section: str
    path: list[str]
    chunk_index: int
    
class FaqResponse(BaseResponse):
    content: str

class SearchBody(SearchOptions):
    question: str