from sqlmodel import SQLModel, Session
from utils import get_engine, get_env
from models import (
    avaliacao,
    categoria,
    endereco,
    estoque,
    item_pedido,
    pagamento,
    papel,
    pedido,
    produto,
    produto_categoria,
    usuario_papel,
    user,
)

DATABASE_URI = get_env('DATABASE_URI')
engine = get_engine(url=DATABASE_URI, echo=False)


def create_database():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(bind=engine) as session:
        yield session
