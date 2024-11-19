from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from dto.user_dto import (
    # Запросы
    UserRegisterRequest, UserLoginRequest,
    # Ответы
    UserTokenResponse, UserDB
)
from services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/profile")
async def get_profile(token: Annotated[str, Depends(oauth2_scheme)]) -> UserDB:
    return await user_service.get_profile(token)


@router.get("/")
async def get_all_users() -> list[UserDB]:
    return await user_service.get_all()


@router.post("/", status_code=201)
async def create_user(dto: UserRegisterRequest) -> UserTokenResponse:
    return await user_service.register(dto)


@router.post("/login")
async def login_user(dto: UserLoginRequest) -> UserTokenResponse:
    return await user_service.login(dto)
