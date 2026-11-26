from functools import lru_cache
from fastapi import Depends
from typing import cast, Any, Annotated
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlmodel import select, func
from app.core.db import SessionDep
from app.configs.faq import FaqSettingsDep
from app.dtos import RCreateFaqPayload, RFaqSearchOptions, RFaqSearchPayload
from pydantic import BaseModel
from app.models.faq import Faq
from app.core.repository import Repository

class FaqRepository(Repository[Faq]):
    entity = Faq

    def __init__(self, settings: FaqSettingsDep, session: SessionDep):
        super().__init__(session)

        self.settings = settings

    def create(self, payload: RCreateFaqPayload):
        return self.executor(lambda: self.create_(payload))

    def search_document(self, search_payload: RFaqSearchPayload, search_options: RFaqSearchOptions):
        return self.executor(lambda: self.search_document_(search_payload, search_options))
        
    def search_document_(self, search_payload: RFaqSearchPayload, search_options: RFaqSearchOptions):
        embedding_col = cast(Any, Faq.embedding)
        max_distance = 1 - search_payload.min_confidence
        dist = embedding_col.cosine_distance(search_payload.question)

        stmt = (
            select(
                Faq.content,
                dist,
            )
            .where(dist <= max_distance)
            .order_by(dist, Faq.chunk_index)
            .limit(search_options.limit)
        )
        return self.session.exec(stmt).all()

@lru_cache
def get_faq_repository(settings: FaqSettingsDep, session: SessionDep):
    return FaqRepository(settings, session)

FaqRepositoryDep = Annotated[FaqRepository, Depends(get_faq_repository)]