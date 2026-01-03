import pytest

@pytest.mark.asyncio
async def test_500_error_sanitized(async_client):
    response = await async_client.get("/boom")

    assert response.status_code == 500
    body = response.json()

    assert body["error"] == "Internal server error"
    assert "traceback" not in str(body)
    assert "request_id" in body
