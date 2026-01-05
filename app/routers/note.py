from fastapi import APIRouter, Depends
from app.schemas.note import NoteCreate, NoteResponse
from app.schemas.response import APIResponse
from app.services.note_service import NoteService
from app.db.database import get_db

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=APIResponse[NoteResponse])
async def create_note(note: NoteCreate, db=Depends(get_db)):
    created = await NoteService.create_note(db, note)
    return {
        "success": True,
        "data": created,
        "request_id": "auto"
    }


@router.get("/", response_model=APIResponse[list[NoteResponse]])
async def list_notes(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    notes = await NoteService.list_notes(db, skip, limit)
    return {
        "success": True,
        "data": notes,
        "request_id": "auto"
    }


# @router.get("/{note_id}")
# async def get_note(
#     note_id: int,
#     request: Request,
#     db: AsyncSession = Depends(get_db),
# ):
#     note = await service.get_note(db, note_id)
#     if not note:
#         raise HTTPException(status_code=404, detail="Note not found")
#     return success_response(data=note, request=request)
