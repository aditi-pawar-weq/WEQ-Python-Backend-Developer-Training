from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.note import NoteCreate, NoteResponse
from app.services.note_service import NoteService
from app.utils.response import success_response

router = APIRouter(prefix="/notes", tags=["Notes"])
service = NoteService()


@router.post("/")
async def create_note(
    request: Request,
    data: NoteCreate,
    db: AsyncSession = Depends(get_db),
):
    note = await service.create_note(db, data)
    return success_response(data=note, request=request)


@router.get("/")
async def list_notes(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    notes = await service.list_notes(db)
    return success_response(data=notes, request=request)


@router.get("/{note_id}")
async def get_note(
    note_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    note = await service.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return success_response(data=note, request=request)
