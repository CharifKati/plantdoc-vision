"""
rate_limiter.py
---------------
Caps requests per IP to prevent abuse and model stealing.
Someone trying to reverse-engineer the model by sending thousands
of images gets cut off at 10 requests per minute.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from fastapi import Request

# Keyed by IP address
limiter = Limiter(key_func=get_remote_address)

# Default limit applied to the /predict endpoint
PREDICT_LIMIT = "10/minute"


def rate_limit_exceeded_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Custom response when the limit is hit.
    Register this in main.py:
        from slowapi.errors import RateLimitExceeded
        app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    """
    ip = get_remote_address(request)
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too many requests",
            "detail": f"Limit is {PREDICT_LIMIT}. Try again in 60 seconds.",
        }
    )
