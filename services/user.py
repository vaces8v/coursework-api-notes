from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from dto.user_dto import UserRegisterRequest, UserLoginRequest
from models.users import User
from database.base_crud import BaseCRUD
from security import hash_password, create_perpetual_token, verify_password, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCRUD(BaseCRUD):
    model = User


async def get_all():
    return await UserCRUD.find_all()


async def register(data: UserRegisterRequest):
    if await UserCRUD.find_one_or_none(email=data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email уже используется')
    hashed_password = hash_password(data.password)
    user_id = await UserCRUD.create_and_return_id(name=data.name, last_name=data.last_name, email=data.email,
                                                  password_hash=hashed_password)
    token = create_perpetual_token({"sub": str(user_id)})
    return {"token": token}


async def login(data: UserLoginRequest):
    user = await UserCRUD.find_one_or_none(email=data.email)
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные")
    token = create_perpetual_token({"sub": str(user.id)})
    return {"token": token}


async def get_profile(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Не валидный токен")

    user = await UserCRUD.find_one_or_none(id=int(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user