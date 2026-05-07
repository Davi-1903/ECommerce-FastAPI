from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_database

from controllers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
