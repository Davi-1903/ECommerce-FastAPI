from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_database

from routes import (
    auth, avaliacoes, categorias, enderecos, estoque,
    pagamentos, papeis, pedidos, produtos, usuarios
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(usuarios.router)
app.include_router(papeis.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(enderecos.router)
app.include_router(avaliacoes.router)
app.include_router(categorias.router)
app.include_router(pagamentos.router)
app.include_router(estoque.router)
app.include_router(auth.router)
