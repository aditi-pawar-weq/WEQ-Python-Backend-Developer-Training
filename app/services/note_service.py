from app.repositories.note_repository import NoteRepository

class NoteService:
    @staticmethod
    async def create_note(db, data):
        repo = NoteRepository()
        return await repo.create(db, title=data.title, content=data.content)

    @staticmethod
    async def list_notes(db, skip: int, limit: int):
        return await NoteRepository.get_notes(db, skip, limit)