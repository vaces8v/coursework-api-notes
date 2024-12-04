from fastapi import HTTPException
from database.base_crud import BaseCRUD
from database.database import async_session_maker
from dto.tag_dto import TagRequest, TagDB
from models.notes import Tag, Note, NotesTags
from security import decode_access_token
from services.user import UserCRUD
from sqlalchemy import select


class TagCRUD(BaseCRUD):
    model = Tag


async def get_all() -> list[TagDB]:
    tags = await TagCRUD.find_all()
    return tags


async def remove_tag(id_tag: int, token: str):
    if token:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Не валидный токен")
        user_id = payload.get("sub")
        if not isinstance(user_id, str) or not user_id:
            raise HTTPException(status_code=401, detail="Не валидный токен")
        user = await UserCRUD.find_one_or_none(id=int(user_id))
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Нет доступа")
        async with async_session_maker() as session:
            notes_associated = await session.execute(
                select(Note).join(NotesTags).filter(NotesTags.tag_id == id_tag)
            )
            notes_to_delete = notes_associated.scalars().all()

            for note in notes_to_delete:
                await session.delete(note)

            await TagCRUD.delete(model_id=id_tag)
        return {"ok": True}
    else:
        return {"ok": False}


async def create_tag(data: TagRequest):
    tag_id = await TagCRUD.create_and_return_id(name=data.name, color=data.color)
    new_tag = await TagCRUD.find_one_or_none(id=tag_id)
    return new_tag
