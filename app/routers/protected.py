from fastapi import APIRouter, Depends, Request

from app.services.auth_service import get_current_user
from app.utils.response import success_response

router = APIRouter()


@router.get("/protected")
async def protected(request: Request, user: str = Depends(get_current_user)):
    data = {"message": "protected content", "user": user}
    return success_response(data=data, request=request)
