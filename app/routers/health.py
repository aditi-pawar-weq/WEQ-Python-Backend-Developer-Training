from fastapi import APIRouter, Request
from app.services.health_service import HealthService
from app.utils.response import success_response

router = APIRouter(prefix="/health", tags=["Health"])
service = HealthService()


@router.get("/ping")
async def ping(request: Request):
    result = await service.ping()
    return success_response(data=result, request=request)


@router.get("/live")
async def live(request: Request):
    result = await service.live()
    return success_response(data=result, request=request)


@router.get("/ready")
async def ready(request: Request):
    result = await service.ready()
    return success_response(data=result, request=request)
