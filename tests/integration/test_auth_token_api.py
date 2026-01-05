import pytest

from app.services.auth_service import create_access_token


@pytest.mark.asyncio
async def test_token_endpoint_and_use(async_client):
    # invalid creds
    r = await async_client.post("/auth/token", json={"username": "aditipawar", "password": "wrong"})
    assert r.status_code == 401

    # valid creds -> returns token
    # register the user first (new registration schema)
    r_reg = await async_client.post("/auth/register", json={"email": "aditi@example.com", "name": "Aditi", "password": "Aditi123"})
    assert r_reg.status_code == 200

    r = await async_client.post("/auth/token", json={"username": "aditi@example.com", "password": "Aditi123"})
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    token = body["data"]["access_token"]
    assert token

    # Use token to call protected endpoint
    r2 = await async_client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    b2 = r2.json()
    assert b2["data"]["user"] == "aditi@example.com"
