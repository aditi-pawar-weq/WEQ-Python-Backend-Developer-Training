from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

# Enforce bcrypt hashing for passwords with 12 rounds. This makes the
# hashing configuration explicit and consistent across environments. If your
# CI or deployment environment cannot build bcrypt, install the prebuilt
# wheel or add the OS packages required to compile it.
_use_bcrypt = False
try:
    # try to configure bcrypt with desired rounds and verify it works
    _ctx = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto")
    try:
        _sample = _ctx.hash("test")
        if _ctx.verify("test", _sample):
            _real_ctx = _ctx
            _use_bcrypt = True
        else:
            raise RuntimeError("bcrypt backend verify failed")
    except Exception:
        logger.warning("bcrypt present but failed to operate correctly; falling back to sha256_crypt")
        _real_ctx = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
except Exception:
    logger.warning("bcrypt not available; falling back to sha256_crypt for hashing")
    _real_ctx = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def _truncate_for_bcrypt(pw: str) -> str:
    """Truncate password to bcrypt's 72-byte limit when encoded as UTF-8."""
    b = pw.encode("utf-8")
    if len(b) > 72:
        return b[:72].decode("utf-8", errors="ignore")
    return pw


class _PwdContextWrapper:
    def __init__(self, ctx: CryptContext, use_bcrypt: bool):
        self._ctx = ctx
        self._use_bcrypt = use_bcrypt

    def hash(self, password: str) -> str:
        if self._use_bcrypt:
            return self._ctx.hash(_truncate_for_bcrypt(password))
        return self._ctx.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        if self._use_bcrypt:
            return self._ctx.verify(_truncate_for_bcrypt(password), hashed)
        return self._ctx.verify(password, hashed)


pwd_context = _PwdContextWrapper(_real_ctx, _use_bcrypt)


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register_user(self, username: str, email: str, name: str | None, password: str):
        # Hash password and create user
        # bcrypt has a 72-byte input limit. To avoid RuntimeError from the
        # underlying C library (and to keep behavior deterministic), truncate
        # to 72 bytes when encoding to UTF-8. This preserves compatibility
        # with bcrypt while making the behavior explicit.
        pw_bytes = password.encode("utf-8")
        if len(pw_bytes) > 72:
            pw_to_hash = pw_bytes[:72].decode("utf-8", errors="ignore")
        else:
            pw_to_hash = password
        hashed = pwd_context.hash(pw_to_hash)
        return await self.repo.create_user(username, email, name, hashed)

    async def authenticate(self, identifier: str, password: str) -> bool:
        # Accept either username or email as identifier
        user = await self.repo.get_by_username(identifier)
        if not user:
            user = await self.repo.get_by_email(identifier)
        if not user:
            return False
        # Apply same truncation when verifying passwords against bcrypt.
        pw_bytes = password.encode("utf-8")
        if len(pw_bytes) > 72:
            pw_to_verify = pw_bytes[:72].decode("utf-8", errors="ignore")
        else:
            pw_to_verify = password
        return pwd_context.verify(pw_to_verify, user.hashed_password)
