from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, StrictStr, Field
from pydantic import field_validator
from app.services.auth_service import create_access_token, get_current_user
from app.services.user_service import UserService
from app.utils.response import success_response
from app.config.settings import settings
from app.db.database import get_db
from app.utils.rate_limiter import RateLimiter
from fastapi import Response
from app.repositories.token_repository import TokenRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

router = APIRouter()

# Simple in-memory limiter (demo only). Limits to 5 attempts per 60 seconds.
limiter = RateLimiter(limit=5, window_seconds=60)


class TokenRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    # using plain str for email to avoid external dependency on email-validator
    email: str
    password: StrictStr = Field(..., min_length=8)
    name: StrictStr = Field(..., min_length=2, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain number")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        # very small heuristic check to avoid extra dependency
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email address")
        return v


@router.post("/auth/token")
async def token(req: TokenRequest, request: Request, db=Depends(get_db)):
    """Issue a JWT token for registered users.

    Expects `username` and `password` in the body. Verifies credentials
    against stored users.
    """
    # Rate limit by client IP (best-effort). Prefer X-Forwarded-For header
    # so tests can override the key; fallback to request.client.host.
    client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "unknown")

    if not limiter.allow(client_ip):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

    service = UserService(db)
    auth_ok = await service.authenticate(req.username, req.password)
    if not auth_ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(req.username)
    # on successful auth reset limiter for this IP
    limiter.reset(client_ip)
    data = {"access_token": access_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}
    return success_response(data=data, request=request)


@router.post("/auth/logout")
async def logout(request: Request, user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Logout the current user by blacklisting their token."""
    token = getattr(request.state, "token", None)
    if not token:
        # fallback: try to read Authorization header
        auth = request.headers.get("authorization") or request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
        token = auth.split(" ", 1)[1]

    repo = TokenRepository(db)
    await repo.add_revoked(token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/auth/register")
async def register(reg: RegisterRequest, request: Request, db=Depends(get_db)):
    """Register a new user (production-style).

    Accepts email, name and password. Returns an access token on success.
    """
    service = UserService(db)
    # check duplicate email
    existing = await service.repo.get_by_email(reg.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    # Use email as username internally to preserve compatibility
    username = reg.email
    user = await service.register_user(username=username, email=reg.email, name=reg.name, password=reg.password)

    # create token and return it with user info (no password)
    access_token = create_access_token(user.username)
    data = {"access_token": access_token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "name": user.name}}
    return success_response(data=data, request=request)


@router.get("/auth/profile")
async def profile(request: Request, user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Return the current user's profile (id, email, name)."""
    service = UserService(db)
    # subject is username/email
    u = await service.repo.get_by_username(user)
    if not u:
        u = await service.repo.get_by_email(user)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    data = {"id": u.id, "email": u.email, "name": u.name}
    return success_response(data=data, request=request)
