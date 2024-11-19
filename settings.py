from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()