from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controllers import routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cwnotes.ru"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


for router in routers:
    app.include_router(router, prefix="/api")