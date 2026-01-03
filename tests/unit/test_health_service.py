import pytest
from app.services.health_service import HealthService


@pytest.mark.asyncio
async def test_ping():
    service = HealthService()
    result = await service.ping()
    assert result["status"] == "ok"


@pytest.mark.asyncio
async def test_live_contains_timestamp():
    service = HealthService()
    result = await service.live()
    assert "timestamp" in result


@pytest.mark.asyncio
async def test_ready():
    service = HealthService()
    result = await service.ready()
    assert result["status"] == "ready"
