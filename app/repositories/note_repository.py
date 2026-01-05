from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.note import Note


class NoteRepository:

    async def create(self, db: AsyncSession, title: str, content: str):
        note = Note(title=title, content=content)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Note))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, note_id: int):
        result = await db.execute(
            select(Note).where(Note.id == note_id)
        )
        return result.scalar_one_or_none()
