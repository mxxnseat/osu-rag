from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sentence_transformers import SentenceTransformer

from app.configs.models import ModelsSettingsDep

class LLMService():
    def __init__(self, models_settings: ModelsSettingsDep):
        self.model = SentenceTransformer(models_settings.embedding_model)

    def encode(self, text: str):
        return self.model.encode(text, normalize_embeddings=True).tolist()

@lru_cache
def get_llm_service(models_settings: ModelsSettingsDep) -> LLMService:
    return LLMService(models_settings)

LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]
