from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controllers import routers

app = FastAPI()

# Настройка CORS
origins = ["https://cwnotes.ru"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["Content-Length"],
    max_age=3600,
)

for router in routers:
    app.include_router(router, prefix="/api")