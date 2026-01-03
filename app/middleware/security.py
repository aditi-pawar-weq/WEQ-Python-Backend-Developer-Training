import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state so it can be used in logging and error handling
        request.state.request_id = request_id
        
        # Process the request
        response = await call_next(request)
        
        # Add security headers to response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        
        return response