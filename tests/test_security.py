import pytest

@pytest.mark.asyncio
async def test_request_id_header(async_client):
    response = await async_client.get("/boom")

    assert "X-Request-ID" in response.headers

@pytest.mark.asyncio
async def test_security_headers_present(async_client):
    response = await async_client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "X-Request-ID" in response.headers
