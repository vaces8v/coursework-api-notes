from datetime import datetime

from pydantic import BaseModel

class TagDB(BaseModel):
    id: int
    name: str
    color: str
    created_at: datetime
    updated_at: datetime


class TagRequest(BaseModel):
    name: str
    color: str