from typing import cast
from app.core.errors import DatabaseError
import pytest
from sqlalchemy.sql.functions import count
from app.models.faq import Faq
from sqlmodel import Session, select, column
from app.services.faq import FaqService
from app.dtos.faq import AddFaqBody

pytestmark = pytest.mark.integration

def faqs_count(session):
    stmt = (
        select(count("*"))
        .select_from(Faq)
    )
    return session.exec(stmt).one()

def test_add(faq_service: FaqService, db_session: Session):
    payload = AddFaqBody(content="content", title="title", chunk_index=0, section="section", path=["section"])
    faq_service.add(payload)

    count_ = faqs_count(db_session)
    assert count_ == 1

def test_add_duplicate(faq_service: FaqService, db_session: Session):
    payload = AddFaqBody(content="content", title="title", chunk_index=0,
                         section="section", path=["section"])

    faq_service.add(payload)

    exc = faq_service.add(payload)
    assert isinstance(exc, DatabaseError)
    assert exc.code == "DUPLICATE_KEY"

    count_ = faqs_count(db_session)
    assert count_ == 1

