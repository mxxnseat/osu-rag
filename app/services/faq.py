from app.repositories.faq import FaqRepositoryDep
from functools import lru_cache
from sqlalchemy.dialects.postgresql import aggregate_order_by
from app.core.errors import DatabaseError, DuplicateKeyError
from blake3 import blake3
import json
from typing import Annotated, Any, cast

from fastapi import Depends
from sqlmodel import column, select, func

from app.configs.faq import FaqSettingsDep
from app.core.db import SessionDep
from app.dtos import AddFaqBody,FaqResponse, RCreateFaqPayload, RFaqSearchPayload, RFaqSearchOptions, FaqSearchPayload
from app.models.faq import Faq
from .llm import LLMServiceDep
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg import errors

class FaqService:
    def __init__(self, settings: FaqSettingsDep, session: SessionDep, llm_service: LLMServiceDep, faq_repository: FaqRepositoryDep):
        self.session = session
        self.llm_service = llm_service
        self.settings = settings
        self.faq_repository = faq_repository

    def add(self, payload: AddFaqBody) -> Faq | DatabaseError:
        embedding_text = "<".join(payload.path)
        embedding_text += f"\r\n\n{payload.content}"
        emb = self.llm_service.encode(embedding_text)
        return self.faq_repository.create(RCreateFaqPayload(
            **payload.model_dump(),
            embedding=emb,
            hash=self.generate_faq_hash(payload)
        ))

    def generate_faq_hash(self, payload: AddFaqBody):
        data = json.dumps(payload.model_dump_json(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return blake3(data.encode("utf-8")).hexdigest()

    def search(self, payload: FaqSearchPayload):
        results = self.faq_repository.search_document(
            RFaqSearchPayload(question=self.llm_service.encode(payload.question), min_confidence=self.settings.min_confidence),
            RFaqSearchOptions(limit=self.settings.relevance_count)
        )
        if isinstance(results, DatabaseError):
            return results
        answer = self.llm_service.answer(payload.question, [row.content for row in results])
        return FaqResponse(content=answer)

@lru_cache
def get_faq_service(settings: FaqSettingsDep, session: SessionDep, llm_service: LLMServiceDep, faq_repository: FaqRepositoryDep):
    return FaqService(settings, session, llm_service, faq_repository)

FaqServiceDep = Annotated[FaqService, Depends(get_faq_service)]
