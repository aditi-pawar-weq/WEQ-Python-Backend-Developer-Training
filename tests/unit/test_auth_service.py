from datetime import timedelta

from app.services.auth_service import create_access_token, decode_token


def test_create_and_decode_token():
    token = create_access_token("alice", expires_delta=timedelta(minutes=5))
    payload = decode_token(token)
    assert payload.get("sub") == "alice"
