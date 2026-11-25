from pydantic import BaseModel

class BaseBody(BaseModel):
    model_config = {"extra": "forbid"}

class BaseResponse(BaseModel):
    model_config = {"extra": "ignore"}

    id: int

class SearchOptions(BaseBody):
    limit:int = 20