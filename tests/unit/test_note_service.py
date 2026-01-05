import pytest
from app.services.note_service import NoteService
from app.schemas.note import NoteCreate
from app.db.test_database import AsyncSessionTest


@pytest.mark.asyncio
async def test_create_note_service():
    service = NoteService()

    async with AsyncSessionTest() as db:
        data = NoteCreate(
            title="Service Title",
            content="Service Content"
        )

        note = await service.create_note(db, data)

        assert note.id is not None
        assert note.title == "Service Title"
