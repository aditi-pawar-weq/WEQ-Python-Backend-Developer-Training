from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> User | None:
        q = select(User).where(User.username == username)
        res = await self.db.execute(q)
        return res.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        q = select(User).where(User.email == email)
        res = await self.db.execute(q)
        return res.scalars().first()

    async def create_user(self, username: str, email: str, name: str | None, hashed_password: str) -> User:
        user = User(username=username, email=email, name=name, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
