from typing import Annotated, Any, cast

from fastapi import Depends
from sqlmodel import column, select

from app.core.db import SessionDep
from app.dtos import AddFaqBody, SearchBody
from app.models.faq import Faq
from .llm import LLMServiceDep

class FaqService:
    def __init__(self, session: SessionDep, llm_service: LLMServiceDep):
        self.session = session
        self.llm_service = llm_service

    def add(self, payload: AddFaqBody):
        emb = self.llm_service.encode(payload.question)
        faq = Faq(question=payload.question, answer=payload.answer, embedding=emb)
        self.session.add(faq)
        self.session.commit()
        return faq

    def search(self, payload: SearchBody):
        q = self.llm_service.encode(payload.question)
        embedding_col = cast(Any, Faq.embedding)

        max_distance = 1 - 0.5
        dist = embedding_col.cosine_distance(q)
        stmt = (
            select(Faq, dist.label("dist"), column("id"), column("answer"))
            .where(dist <= max_distance)
            .order_by("dist")
            .limit(payload.limit)
        )
        result = self.session.exec(stmt).all()
        return result
    
def get_faq_service(session: SessionDep, llm_service: LLMServiceDep):
    return FaqService(session, llm_service)

FaqServiceDep = Annotated[FaqService, Depends(get_faq_service)]