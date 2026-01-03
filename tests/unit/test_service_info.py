import pytest
from app.services.service_info import ServiceInfoService


@pytest.mark.asyncio
async def test_service_info():
    service = ServiceInfoService()
    result = await service.get_info()

    assert "name" in result
    assert "environment" in result
    assert "version" in result


@pytest.mark.asyncio
async def test_service_time():
    service = ServiceInfoService()
    result = await service.get_time()

    assert "server_time" in result
