from typing import Annotated, Any, cast

from fastapi import Depends
from sqlmodel import column, select

from app.configs.faq import FaqSettingsDep
from app.core.db import SessionDep
from app.dtos import AddFaqBody, SearchBody
from app.models.faq import Faq
from .llm import LLMServiceDep

class FaqService:
    def __init__(self, settings: FaqSettingsDep, session: SessionDep, llm_service: LLMServiceDep):
        self.session = session
        self.llm_service = llm_service
        self.settings = settings

    def add(self, payload: AddFaqBody):
        embedding_text = "<".join(payload.path)
        embedding_text += f"\r\n\n{payload.content}"
        emb = self.llm_service.encode(embedding_text)
        faq = Faq(
            title=payload.title, 
            section=payload.section, 
            content=payload.content, 
            embedding=emb,
            chunk_index=payload.chunk_index
        )
        self.session.add(faq)
        self.session.commit()
        return faq

    def search(self, payload: SearchBody):
        q = self.llm_service.encode(payload.question)
        embedding_col = cast(Any, Faq.embedding)

        max_distance = 1 - self.settings.min_confidence
        dist = embedding_col.cosine_distance(q)
        stmt = (
            select(Faq, dist.label("dist"), column("id"), column("content"))
            .where(dist <= max_distance)
            .order_by("dist")
            .limit(payload.limit)
        )
        results = self.session.exec(stmt).all()
        self.llm_service.answer(payload.question, [result[0].content for result in results])
        return results
    
def get_faq_service(settings: FaqSettingsDep, session: SessionDep, llm_service: LLMServiceDep):
    return FaqService(settings, session, llm_service)

FaqServiceDep = Annotated[FaqService, Depends(get_faq_service)]
