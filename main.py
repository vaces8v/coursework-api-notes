from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controllers import routers

app = FastAPI()

origins = ["https://cwnotes.ru"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cwnotes.ru", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

for router in routers:
    app.include_router(router, prefix="/api")