import pytest


@pytest.mark.asyncio
async def test_health_ping(async_client):
    response = await async_client.get("/health/ping")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert "request_id" in body
