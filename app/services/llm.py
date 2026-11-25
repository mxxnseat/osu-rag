from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sentence_transformers import SentenceTransformer
from transformers import pipeline

from app.configs.models import ModelsSettingsDep

class LLMService():
    def __init__(self, models_settings: ModelsSettingsDep):
        self.embedding_model = SentenceTransformer(models_settings.embedding_model)
        self.llm = pipeline("text-generation", model=models_settings.llm_model, device="cuda")
        print(self.llm.model.dtype)
        
    def encode(self, text: str):
        return self.embedding_model.encode(text, normalize_embeddings=True).tolist()

    def answer(self, question: str, chunks: list[str]):
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": f"""
                Answer only from the context below. If the context doesn't directly
                answer the question, say "I don't know". Mentioning a term is not
                the same as defining it.

                Context: {chunks}
                Question: {question}
                """}
            ]},
        ]
        out = self.llm(messages, max_new_tokens=512) # type: ignore
        print(out[0]["generated_text"][-1]["content"])

@lru_cache
def get_llm_service(models_settings: ModelsSettingsDep) -> LLMService:
    return LLMService(models_settings)

LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]
