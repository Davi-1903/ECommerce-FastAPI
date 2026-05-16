from sqlmodel import SQLModel, Session, create_engine
from utils import get_env
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
engine = create_engine(DATABASE_URI, echo=False)


def create_database():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(bind=engine) as session:
        yield session
