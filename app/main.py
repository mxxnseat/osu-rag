from app.exception_handlers.common_handler import common_exception_handler
from fastapi import FastAPI
from .routers.faq import router as faq_router

app = FastAPI()

app.exception_handler(Exception)(common_exception_handler)

app.include_router(faq_router)

@app.get("/health/liveness")
def root():
    return {"status": "ok"}
