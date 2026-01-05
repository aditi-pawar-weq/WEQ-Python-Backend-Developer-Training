from datetime import datetime, timedelta, timezone
from typing import Any

import importlib
from fastapi import Request, HTTPException, status, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.token_repository import TokenRepository

from app.config.settings import settings


# Resolve jwt module and support PyJWT-like API. We'll also try to access
# get_unverified_header so we can inspect `kid` before verification.
_jwt = importlib.import_module("jwt")
_encode = getattr(_jwt, "encode", None)
_decode = getattr(_jwt, "decode", None)
_get_unverified_header = getattr(_jwt, "get_unverified_header", None)

if _encode is None or _decode is None:
    try:
        from jwt.api_jwt import PyJWT

        _pyjwt = PyJWT()
        _encode = _pyjwt.encode
        _decode = _pyjwt.decode
        _get_unverified_header = getattr(_pyjwt, "get_unverified_header", None)
    except Exception:
        _encode = None
        _decode = None
        _get_unverified_header = None


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if _encode is None:
        raise RuntimeError("No usable JWT implementation found. Install PyJWT.")

    now = datetime.now(timezone.utc)
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + expires_delta
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "aud": settings.JWT_AUDIENCE,
        "iss": settings.JWT_ISSUER,
    }

    # Determine active key and include kid in header for rotation
    kid = getattr(settings, "ACTIVE_KEY_ID", None)
    key = settings.JWT_KEYS.get(kid) if kid else None
    if not key:
        # Fallback to first value in JWT_KEYS
        key = next(iter(settings.JWT_KEYS.values()))
        kid = next(iter(settings.JWT_KEYS.keys()))

    headers = {"kid": kid} if kid else None

    token = _encode(payload, key, algorithm=settings.JWT_ALGORITHM, headers=headers) if headers else _encode(payload, key, algorithm=settings.JWT_ALGORITHM)
    return token


def _select_key_for_token(token: str) -> str:
    """Extract kid from token header without verifying signature and return the configured secret."""
    kid = None
    if _get_unverified_header is not None:
        try:
            hdr = _get_unverified_header(token)
            kid = hdr.get("kid")
        except Exception:
            kid = None

    if kid and kid in settings.JWT_KEYS:
        return settings.JWT_KEYS[kid]

    # fallback: use active key
    return settings.JWT_KEYS.get(getattr(settings, "ACTIVE_KEY_ID", next(iter(settings.JWT_KEYS.keys()))))


def decode_token(token: str) -> dict[str, Any]:
    if _decode is None:
        raise RuntimeError("No usable JWT implementation found. Install PyJWT.")

    # Select proper secret using kid if present
    key = _select_key_for_token(token)

    try:
        # Validate audience and issuer explicitly
        payload = _decode(
            token,
            key,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
        return payload
    except Exception:
        # Map any decode/validation error to a 401 for the API.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    request: Request = None,
    db: AsyncSession = Depends(get_db),
):
    """Dependency to retrieve current user from Authorization header.

    This uses the HTTP Bearer security scheme so the OpenAPI UI will show
    an "Authorize" button where you can paste a Bearer token.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")

    token = credentials.credentials
    payload = decode_token(token)
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # check blacklist
    repo = TokenRepository(db)
    if await repo.is_revoked(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    if request is not None:
        request.state.user = subject
        request.state.token = token
    return subject
