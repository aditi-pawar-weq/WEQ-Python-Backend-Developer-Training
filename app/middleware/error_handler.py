import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("weq")


async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # Log a concise error message without dumping the full traceback to logs.
        # The traceback can contain sensitive information and tests verify the
        # response body is sanitized. Include the exception message and the
        # request_id so logs are still useful for correlating incidents.
        request_id = getattr(request.state, "request_id", None)
        if request_id:
            logger.error("Unhandled error: %s (request_id=%s)", str(exc), request_id)
        else:
            logger.error("Unhandled error: %s", str(exc))
        
        # Get request ID from request state (already computed above)
        
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