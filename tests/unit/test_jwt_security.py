import importlib
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.config.settings import settings
from app.services.auth_service import create_access_token, decode_token


def _jwt_encode(payload: dict, key: str, headers: dict | None = None) -> str:
    jwt = importlib.import_module("jwt")
    # Some jwt implementations return bytes
    token = jwt.encode(payload, key, algorithm=settings.JWT_ALGORITHM, headers=headers)
    if isinstance(token, bytes):
        token = token.decode()
    return token


def test_missing_audience_rejected():
    # craft a token without 'aud' claim
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "user-x",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=5)).timestamp()),
    }
    # Use the active key from settings
    active_kid = getattr(settings, "ACTIVE_KEY_ID", None)
    key = settings.JWT_KEYS.get(active_kid) if active_kid else next(iter(settings.JWT_KEYS.values()))

    token = _jwt_encode(payload, key)

    with pytest.raises(HTTPException):
        decode_token(token)


def test_tampered_token_rejected():
    token = create_access_token("tamper-test", expires_delta=timedelta(minutes=5))
    # tamper by altering the token string
    tampered = token[:-6] + ("ABCDEF" if not token.endswith("ABCDEF") else "XXXXXX")

    with pytest.raises(HTTPException):
        decode_token(tampered)


def test_kid_rotation_selects_correct_key(monkeypatch):
    # Prepare two keys and set active to key-1
    keys = {
        "key-1": "secret-one",
        "key-2": "secret-two",
    }
    monkeypatch.setattr(settings, "JWT_KEYS", keys, raising=False)
    monkeypatch.setattr(settings, "ACTIVE_KEY_ID", "key-1", raising=False)

    # Manually sign a token using key-2 and include kid header
    now = datetime.now(timezone.utc)
    payload = {
        "sub": "rotated-user",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=10)).timestamp()),
        "aud": settings.JWT_AUDIENCE,
        "iss": settings.JWT_ISSUER,
    }

    token = _jwt_encode(payload, keys["key-2"], headers={"kid": "key-2"})

    # decode_token should inspect kid and use key-2 to validate
    decoded = decode_token(token)
    assert decoded.get("sub") == "rotated-user"
