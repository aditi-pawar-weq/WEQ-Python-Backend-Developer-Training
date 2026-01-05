import pytest


@pytest.mark.asyncio
async def test_login_rate_limiting(async_client):
    # send 6 invalid attempts; the 6th should be 429
    url = "/auth/token"
    payload = {"username": "noone", "password": "wrong"}
    status_codes = []
    for i in range(6):
        # set a test header to isolate the IP key from other tests
        r = await async_client.post(url, json=payload, headers={"x-forwarded-for": "9.9.9.9"})
        status_codes.append(r.status_code)

    # first 5 should be 401 (invalid creds), 6th should be 429
    assert status_codes[:5] == [401, 401, 401, 401, 401]
    assert status_codes[5] == 429
