import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("weq")


async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error("Unhandled error", exc_info=exc)
        
        # Get request ID from request state
        request_id = getattr(request.state, "request_id", None)
        
        # Create error response with request_id in the body
        response = JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "request_id": request_id
            }
        )
        
        # Also add request ID to response headers
        if request_id:
            response.headers["X-Request-ID"] = request_id
        
        return response