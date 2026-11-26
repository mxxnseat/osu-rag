from app.core.errors import DuplicateKeyError, DatabaseError
from typing import Annotated

from fastapi import status, APIRouter, Body, Query, HTTPException

from app.dtos import FaqResponse, FaqSearchPayload, AddFaqBody
from app.services.faq import FaqServiceDep

router = APIRouter(prefix="/faq", tags=["faq"])

@router.get("/search", response_model=FaqResponse)
def search(faq_service: FaqServiceDep, search_body: Annotated[FaqSearchPayload, Query()]):
    res = faq_service.search(search_body)
    if isinstance(res, Exception):
        raise res
    return res
