from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.database import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_notes.db"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

AsyncSessionTest = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_test_db():
    async with AsyncSessionTest() as session:
        yield session
