from argon2 import PasswordHasher
from jose import JWTError, jwt
from settings import settings

ph = PasswordHasher()
ALGORITHM = "HS256"


def create_perpetual_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Декодированный payload: {payload}")  # Вывод декодированного payload
        return payload
    except JWTError as e:
        print(f"Ошибка декодирования: {e}")  # Логируем ошибку
        return None


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        return False
