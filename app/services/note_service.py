from app.repositories.note_repository import NoteRepository


class NoteService:

    def __init__(self):
        self.repo = NoteRepository()

    async def create_note(self, db, data):
        return await self.repo.create(
            db,
            title=data.title,
            content=data.content
        )

    async def list_notes(self, db):
        return await self.repo.get_all(db)

    async def get_note(self, db, note_id: int):
        return await self.repo.get_by_id(db, note_id)
