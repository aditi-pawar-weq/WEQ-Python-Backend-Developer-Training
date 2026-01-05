from datetime import timedelta

import pytest

from fastapi import HTTPException

from app.services.auth_service import create_access_token, decode_token


def test_create_and_decode_token_contains_claims():
    token = create_access_token("alice", expires_delta=timedelta(minutes=5))
    payload = decode_token(token)
    assert payload.get("sub") == "alice"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_expired_token_raises():
    # create a token that is already expired
    token = create_access_token("bob", expires_delta=timedelta(seconds=-10))
    with pytest.raises(HTTPException):
        decode_token(token)
