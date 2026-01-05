import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.note_repository import NoteRepository
from app.db.test_database import AsyncSessionTest


@pytest.mark.asyncio
async def test_create_note_repository():
    repo = NoteRepository()

    async with AsyncSessionTest() as db:
        note = await repo.create(
            db,
            title="Test title",
            content="Test content"
        )

        assert note.id is not None
        assert note.title == "Test title"
        assert note.content == "Test content"
