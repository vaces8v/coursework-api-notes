from fastapi import APIRouter

router = APIRouter(tags=["ping"], prefix="/ping")

@router.get("/")
async def ping():
    return {"ping": "pong"}
