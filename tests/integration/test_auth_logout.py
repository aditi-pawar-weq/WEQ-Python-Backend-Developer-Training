import pytest


@pytest.mark.asyncio
async def test_logout_blacklists_token(async_client):
    # register user
    r_reg = await async_client.post("/auth/register", json={"email": "who@example.com", "name": "Who", "password": "Who12345"})
    assert r_reg.status_code == 200

    # get token
    r = await async_client.post("/auth/token", json={"username": "who@example.com", "password": "Who12345"})
    assert r.status_code == 200
    token = r.json()["data"]["access_token"]

    # protected works
    r2 = await async_client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200

    # logout
    r_logout = await async_client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert r_logout.status_code == 204

    # now token should be rejected
    r3 = await async_client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert r3.status_code == 401
