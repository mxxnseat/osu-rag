from fastapi import FastAPI
from .routers.faq import router as faq_router

app = FastAPI()
app.include_router(faq_router)

@app.get("/health/liveness")
def root():
    return {"status": "ok"}
