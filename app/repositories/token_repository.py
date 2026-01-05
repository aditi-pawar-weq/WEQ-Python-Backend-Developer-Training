from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import RevokedToken


class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_revoked(self, token: str) -> bool:
        q = select(RevokedToken).where(RevokedToken.token == token)
        res = await self.db.execute(q)
        return res.scalars().first() is not None

    async def add_revoked(self, token: str) -> RevokedToken:
        r = RevokedToken(token=token)
        self.db.add(r)
        await self.db.commit()
        await self.db.refresh(r)
        return r
