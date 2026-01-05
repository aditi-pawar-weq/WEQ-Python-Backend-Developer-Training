import pytest


@pytest.mark.asyncio
async def test_profile_flow(async_client):
    # register a new user
    resp = await async_client.post("/auth/register", json={
        "email": "profile_user@example.com",
        "password": "StrongPass1",
        "name": "Profile User"
    })
    assert resp.status_code == 200
    token = resp.json()["data"]["access_token"]

    # access profile
    headers = {"Authorization": f"Bearer {token}"}
    resp = await async_client.get("/auth/profile", headers=headers)
    assert resp.status_code == 200
    body = resp.json()["data"]
    assert body["email"] == "profile_user@example.com"
    assert body["name"] == "Profile User"

    # logout (blacklist token)
    resp = await async_client.post("/auth/logout", headers=headers)
    assert resp.status_code == 204

    # further access should be unauthorized
    resp = await async_client.get("/auth/profile", headers=headers)
    assert resp.status_code == 401
