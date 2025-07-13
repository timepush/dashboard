from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback


def format_error(message: str, type_: str, status: int, code: str | None = None):
    body = {
        "error": {
            "message": message,
            "type": type_,
            "status": status
        }
    }
    if code:
        body["error"]["code"] = code
    return JSONResponse(status_code=status, content=body)


async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, (HTTPException, StarletteHTTPException)):
        if getattr(exc, 'status_code', None) == 404:
            return format_error("Not found", "not_found", 404)
        return format_error(str(exc.detail), "http_exception", exc.status_code)

    if isinstance(exc, (RequestValidationError, ValidationError)):
        # Get the first error detail if available
        details = exc.errors() if hasattr(exc, 'errors') else []
        if details:
            first = details[0]
            loc = ".".join(str(x) for x in first.get("loc", []))
            msg = first.get("msg", "Invalid input")
            message = f"{msg} ({loc})"
        else:
            message = "Invalid or missing input data. Please check your input and try again."
        return format_error(message, "validation_error", 422)

    # Generic database or other errors
    traceback.print_exception(type(exc), exc, exc.__traceback__)
    return format_error(str(exc), "internal_error", 500)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, global_exception_handler)
    app.add_exception_handler(StarletteHTTPException, global_exception_handler)
    app.add_exception_handler(RequestValidationError, global_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
