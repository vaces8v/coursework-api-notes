from database.base_crud import BaseCRUD
from dto.tag_dto import TagRequest, TagDB
from models.notes import Tag


class TagCRUD(BaseCRUD):
    model = Tag


async def get_all() -> list[TagDB]:
    tags = await TagCRUD.find_all()
    return tags


async def create_tag(data: TagRequest):
    tag_id = await TagCRUD.create_and_return_id(name=data.name, color=data.color)
    new_tag = await TagCRUD.find_one_or_none(id=tag_id)
    return new_tag
