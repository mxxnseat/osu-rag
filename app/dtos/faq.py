from app.dtos.base import BaseBody, SearchOptions, BaseResponse

class AddFaqBody(BaseBody):
    question: str
    answer: str

class FaqResponse(BaseResponse):
    answer: str

class SearchBody(SearchOptions):
    question: str