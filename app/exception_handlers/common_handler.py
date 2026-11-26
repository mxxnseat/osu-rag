from urllib.request import Request
from app.core.errors import DatabaseError
from fastapi.responses import JSONResponse

def common_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={"error": "database_error", "detail": "Something went wrong"},
    )