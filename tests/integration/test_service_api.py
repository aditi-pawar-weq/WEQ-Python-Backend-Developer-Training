import pytest


@pytest.mark.asyncio
async def test_service_info_api(async_client):
    response = await async_client.get("/service/info")

    assert response.status_code == 200
    body = response.json()

    assert body["success"] is True
    assert "name" in body["data"]
    assert "environment" in body["data"]
    assert "version" in body["data"]
    assert "request_id" in body


@pytest.mark.asyncio
async def test_service_time_api(async_client):
    response = await async_client.get("/service/time")

    assert response.status_code == 200
    body = response.json()

    assert body["success"] is True
    assert "server_time" in body["data"]
    assert "request_id" in body
