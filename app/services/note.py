from fastapi import HTTPException, status

from app.database.base_crud import BaseCRUD
from app.dto.note_dto import NoteCreateRequest, NoteResponse, TagResponse
from app.models.notes import Note, NotesTags
from app.security import decode_access_token
from app.database.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class NoteCRUD(BaseCRUD):
    model = Note

    @classmethod
    async def get_all(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.tags).joinedload(NotesTags.tag))
                .where(cls.model.user_id == user_id, cls.model.is_archive == False)
                .order_by(cls.model.created_at.desc())
            )
            res = await session.execute(query)
            return res.unique().scalars().all()

    @classmethod
    async def get_all_archive(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.tags).joinedload(NotesTags.tag))
                .where(cls.model.user_id == user_id, cls.model.is_archive == True)
                .order_by(cls.model.created_at.desc())
            )
            res = await session.execute(query)
            return res.unique().scalars().all()

    @classmethod
    async def get_one(cls, note_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.tags).joinedload(NotesTags.tag))
                .where(cls.model.id == note_id)
            )
            res = await session.execute(query)
            return res.unique().scalar_one_or_none()


class NoteTagsCRUD(BaseCRUD):
    model = NotesTags


async def get_all_my(token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    notes = await NoteCRUD.get_all(user_id=int(user_id))
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            user_id=note.user_id,
            description=note.description,
            is_archive=note.is_archive,
            created_at=note.created_at,
            updated_at=note.updated_at,
            tags=[
                TagResponse(
                    id=note_tag.tag.id,
                    name=note_tag.tag.name,
                    color=note_tag.tag.color,
                )
                for note_tag in note.tags
            ]
        )
        for note in notes
    ]

async def get_all_my_archives(token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    notes = await NoteCRUD.get_all_archive(user_id=int(user_id))
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            user_id=note.user_id,
            description=note.description,
            is_archive=note.is_archive,
            created_at=note.created_at,
            updated_at=note.updated_at,
            tags=[
                TagResponse(
                    id=note_tag.tag.id,
                    name=note_tag.tag.name,
                    color=note_tag.tag.color,
                )
                for note_tag in note.tags
            ]
        )
        for note in notes
    ]

async def get_by_id(note_id: int) -> NoteResponse:
    note = await NoteCRUD.get_one(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return NoteResponse(
        id=note.id,
        title=note.title,
        user_id=note.user_id,
        description=note.description,
        is_archive=note.is_archive,
        created_at=note.created_at,
        updated_at=note.updated_at,
        tags=[
            TagResponse(
                id=note_tag.tag.id,
                name=note_tag.tag.name,
                color=note_tag.tag.color,
            )
            for note_tag in note.tags
        ]
    )


async def create_note(data: NoteCreateRequest, token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    note_id = await NoteCRUD.create_and_return_id(user_id=int(user_id), title=data.title, description=data.description)

    if data.noteTags:
        for tag_id in data.noteTags:
            await NoteTagsCRUD.create(note_id=note_id, tag_id=tag_id)

    return {"ok": True, "note_id": note_id}


async def delete_by_id(note_id: int, token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    note = await NoteCRUD.find_by_id(model_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if note.user_id != int(user_id):
        raise HTTPException(status_code=403, detail="Изменения не доступны")

    await NoteCRUD.delete(model_id=note_id)


async def archive_add_by_id(note_id: int, token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    note = await NoteCRUD.find_by_id(model_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if note.user_id != int(user_id):
        raise HTTPException(status_code=403, detail="Изменения не доступны")

    await NoteCRUD.update(model_id=note_id, is_archive=True)

async def archive_remove_by_id(note_id: int, token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    note = await NoteCRUD.find_by_id(model_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if note.user_id != int(user_id):
        raise HTTPException(status_code=403, detail="Изменения не доступны")

    await NoteCRUD.update(model_id=note_id, is_archive=False)