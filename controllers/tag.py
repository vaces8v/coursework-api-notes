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