from fastapi import APIRouter
from services import tag as tag_service
from dto.tag_dto import TagRequest, TagDB

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/")
async def get_all_tags() -> list[TagDB]:
    return await tag_service.get_all()

@router.post("/")
async def create_tag(dto: TagRequest):
    return await tag_service.create_tag(dto)

@router.post("/generate/")
async def generate_tags() -> list[TagDB]:
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