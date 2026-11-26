# tests/conftest.py
from app.services.llm import ILLMService, get_llm_service
import os
import pytest
from fastapi.testclient import TestClient
from fastapi_injectable import register_app, run_coroutine_sync
from sqlmodel import Session, SQLModel
from fastapi_injectable import get_injected_obj

from app.services.faq import get_faq_service, FaqService

import app.models  # noqa: F401  (registers your tables)
from app.core.db import create_cached_engine, get_engine, get_session
from app.main import app

TEST_DB_URL = os.environ["TEST_DATABASE_URL"]

@pytest.fixture(scope="session")
def engine():
    engine = create_cached_engine(TEST_DB_URL)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(engine):
    with engine.connect() as conn:
        trans = conn.begin()
        with Session(bind=conn, join_transaction_mode="create_savepoint") as session:
            yield session
        trans.rollback()

class FakeLLMService(ILLMService):
    def encode(self, text: str) -> list[float]:
        return [1.0] + [0.0] * 383  # bge-small has 384 dimensions

    def answer(self, question: str, chunks: list[str]):
        return "fake answer"

@pytest.fixture()
def fake_llm():
    return FakeLLMService()

@pytest.fixture(autouse=True)
def override_db(engine, db_session, fake_llm):
    run_coroutine_sync(register_app(app))
    app.dependency_overrides[get_engine] = lambda: engine
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_llm_service] = lambda: fake_llm
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def faq_service(override_db) -> FaqService:
    return get_injected_obj(get_faq_service)

@pytest.fixture
def client():
    with TestClient(app) as c:  # also runs your lifespan
        yield c
