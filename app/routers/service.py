from fastapi import APIRouter, Request
from app.services.service_info import ServiceInfoService
from app.utils.response import success_response

router = APIRouter(prefix="/service", tags=["Service"])
service = ServiceInfoService()


@router.get("/info")
async def service_info(request: Request):
    result = await service.get_info()
    return success_response(data=result, request=request)


@router.get("/time")
async def service_time(request: Request):
    result = await service.get_time()
    return success_response(data=result, request=request)
