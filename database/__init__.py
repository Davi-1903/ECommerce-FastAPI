from sqlmodel import SQLModel, Session
from utils import create_url, get_engine
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
    usuario,
    usuario_papel,
)

DATABASE_URI = create_url()
engine = get_engine(url=DATABASE_URI, echo=False)


def create_database():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(bind=engine) as session:
        yield session
