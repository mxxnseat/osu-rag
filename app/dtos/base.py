from pydantic import BaseModel

class BaseBody(BaseModel):
    model_config = {"extra": "forbid"}

class BaseRecord(BaseModel):
    model_config = {"extra": "ignore"}
    
    id: int

class BaseResponse(BaseModel):
    model_config = {"extra": "ignore"}

class SearchOptions(BaseBody):
    limit:int = 20