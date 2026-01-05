import pytest

from app.services.auth_service import create_access_token


@pytest.mark.asyncio
async def test_protected_endpoint_requires_auth(async_client):
    # no auth -> 401
    r = await async_client.get("/protected")
    assert r.status_code == 401

    # invalid token -> 401
    r = await async_client.get("/protected", headers={"Authorization": "Bearer badtoken"})
    assert r.status_code == 401

    # valid token -> 200
    token = create_access_token("aditipawar")
    r = await async_client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert body["data"]["user"] == "aditipawar"
