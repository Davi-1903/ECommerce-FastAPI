from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_database

from controllers import catalogo, endereco, papeis, pedidos, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(usuarios.router)
app.include_router(papeis.router)
app.include_router(catalogo.router)
app.include_router(pedidos.router)
app.include_router(endereco.router)
