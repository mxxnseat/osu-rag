from typing import Annotated

from fastapi import status, APIRouter, Body, Query, HTTPException

from app.dtos import FaqResponse, SearchBody, AddFaqBody
from app.services.faq import FaqServiceDep

router = APIRouter(prefix="/faq", tags=["faq"])

@router.get("/search", response_model=list[FaqResponse])
def search(faq_service: FaqServiceDep, search_body: Annotated[SearchBody, Query()]):
    result = faq_service.search(search_body)
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FaqResponse)
def add(faq_service: FaqServiceDep, search_body: Annotated[AddFaqBody, Body()]):
    result = faq_service.add(search_body)
    return result
