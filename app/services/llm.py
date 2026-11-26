from functools import lru_cache
from typing import Annotated, Protocol
import torch as t

from fastapi import Depends
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForMultimodalLM, AutoProcessor, pipeline

from app.configs.models import ModelsSettingsDep

class ILLMService(Protocol):
    def encode(self, text: str): ...
    def answer(self, question: str, chunks: list[str]): ...

class LLMService(ILLMService):
    def __init__(self, models_settings: ModelsSettingsDep):
        self.embedding_model = SentenceTransformer(models_settings.embedding_model)

        self.llm_processor = AutoProcessor.from_pretrained(models_settings.llm_model)

        self.llm = AutoModelForMultimodalLM.from_pretrained(
            models_settings.llm_model,
            dtype=t.bfloat16,
            device_map="cuda"
        )

        self.LLM_SYSTEM_PROMPT = """
You are a context-based question answering system.

RULES:
1. Answer the QUESTION using ONLY the provided CONTEXT.
2. The CONTEXT is your only source of information.
3. Never use your internal knowledge or training data.
4. If the answer is not explicitly stated in the CONTEXT,
   respond EXACTLY with: Sumimasen wakaranai
5. Do not infer, assume, or guess.
6. Answer in at most 3 sentences.
7. Do not explain your reasoning.

IMPORTANT:
An unrelated document does NOT contain an answer.
If the context does not provide sufficient information,
you MUST return: Sumimasen wakaranai.
        """
        
    def encode(self, text: str):
        return self.embedding_model.encode(text, normalize_embeddings=True).tolist()

    def answer(self, question: str, chunks: list[str]):
        user_prompt = self.build_user_prompt(question, chunks)
        messages = [
            {"role": "system", "content": self.LLM_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        inputs = self.llm_processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.llm.device)

        outputs = self.llm.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=False
        )

        generated = outputs[0][inputs["input_ids"].shape[-1]:]

        return self.llm_processor.decode(generated, skip_special_tokens=True)

    def build_user_prompt(self, question: str, chunks: list[str]):
        context = "\n\n".join(
            f"[Document {i + 1}]\n{chunk}"
            for i, chunk in enumerate(chunks)
        )

        return f"""
    CONTEXT:
    {context}
    
    QUESTION:
    {question}
    """

@lru_cache
def get_llm_service(models_settings: ModelsSettingsDep) -> LLMService:
    return LLMService(models_settings)

LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]
