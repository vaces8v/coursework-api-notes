from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dto.note_dto import NoteCreateRequest, NoteResponse

from services import note as note_service

router = APIRouter(prefix="/notes", tags=["notes"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
async def get_all_my_notes(token: Annotated[str, Depends(oauth2_scheme)]):
    return await note_service.get_all_my(token)

@router.get("/{id}")
async def get_by_id(id: int) -> NoteResponse:
    return await note_service.get_by_id(id)

@router.post("/", status_code=201)
async def create_note(dto: NoteCreateRequest, token: Annotated[str, Depends(oauth2_scheme)]):
    return await note_service.create_note(dto, token)

@router.delete("/{note_id}")
async def delete_by_id(note_id: int, token: Annotated[str, Depends(oauth2_scheme)]):
    return await note_service.delete_by_id(note_id, token)