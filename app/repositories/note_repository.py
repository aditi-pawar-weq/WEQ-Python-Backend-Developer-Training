from sqlalchemy.future import select
from app.models.note import Note

class NoteRepository:
    async def create(self, db, title: str, content: str):
        """Create a Note record, commit and refresh so callers get persisted fields.

        Returns the SQLAlchemy Note instance with id and created_at populated.
        """
        note = Note(title=title, content=content)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    @staticmethod
    async def get_notes(db, skip: int, limit: int):
        stmt = select(Note).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
