from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from security import decode_access_token
from services import tag as tag_service
from dto.tag_dto import TagRequest, TagDB
from fastapi.security import OAuth2PasswordBearer

from services.tag import TagCRUD
from services.user import UserCRUD

router = APIRouter(prefix="/tags", tags=["tags"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
async def get_all_tags() -> list[TagDB]:
    return await tag_service.get_all()

@router.post("/")
async def create_tag(dto: TagRequest, token: Annotated[str, Depends(oauth2_scheme)]):
    return await tag_service.create_tag(dto)

@router.delete("/{id_tag}")
async def remove_tag(id_tag: int, token: Annotated[str, Depends(oauth2_scheme)]):
    return await tag_service.remove_tag(id_tag, token)

@router.post("/generate/")
async def generate_tags(token: Annotated[str, Depends(oauth2_scheme)]):
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
        tags = await TagCRUD.find_all()
        if len(tags) > 0:
            raise HTTPException(status_code=400, detail="Теги уже сгенерированы")
        tag_data = [
            ("В процессе", "#FFA500"),
            ("Личное", "#FF6347"),
            ("Работа", "#4682B4"),
            ("Семья", "#FFD700"),
            ("Друзья", "#32CD32"),
            ("Завершено", "#8A2BE2"),
            ("Идеи", "#FF69B4"),
            ("Важно", "#00BFFF"),
            ("Курсы", "#FF4500"),
            ("Проекты", "#2E8B57"),
            ("Задачи", "#B8860B"),
            ("Наброски", "#6A5ACD"),
            ("Напоминания", "#DC143C"),
            ("На заметку", "#FFDAB9"),
            ("Читать", "#00CED1"),
            ("Смотреть", "#FF8C00"),
            ("Покупки", "#ADFF2F"),
            ("Поездки", "#C71585"),
            ("Здоровье", "#8B0000"),
            ("Финансы", "#FFA07A"),
            ("Хобби", "#4682B4"),
        ]

        tags = []
        for name, color in tag_data:
            tag_request = TagRequest(name=name, color=color)
            tag_db = await tag_service.create_tag(tag_request)
            tags.append(tag_db)

        return tags
    else:
        return {"error": "Token was not provided"}