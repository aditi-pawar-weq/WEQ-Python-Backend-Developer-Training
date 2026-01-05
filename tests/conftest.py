import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client


from app.db.database import get_db
from app.db.test_database import get_test_db, engine_test, Base


@pytest.fixture(scope="session", autouse=True)
async def prepare_test_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


app.dependency_overrides[get_db] = get_test_db
