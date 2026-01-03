from typing import Any
from fastapi import Request


def success_response(
    *,
    data: Any,
    request: Request
):
    return {
        "success": True,
        "data": data,
        "request_id": request.state.request_id
    }
