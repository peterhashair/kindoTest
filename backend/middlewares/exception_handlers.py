from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": None,
            "error": exc.detail,
        },
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    # Reformat Pydantic's validation errors for better readability
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_details.append(f"[{field}]: {message}")

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "data": None,
            "error": {"message": "Validation failed", "details": error_details},
        },
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "data": None,
            "error": "An unexpected internal server error occurred.",
        },
    )
