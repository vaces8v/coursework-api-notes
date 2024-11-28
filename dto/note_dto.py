from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class NoteDB(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    is_archive: bool = False
    created_at: datetime
    updated_at: datetime


class NoteCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    noteTags: List[int] = []


class TagResponse(BaseModel):
    id: int
    name: str
    color: str


class NoteUpdateRequest(BaseModel):
    title: str
    description: str
    tags: list[int] = []


class NoteResponse(BaseModel):
    id: int
    title: str
    user_id: int
    description: str | None
    is_archive: bool
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse]
