from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
