from sqlmodel import SQLModel, Session, create_engine
from model import (
    avaliacao, categoria, endereco, estoque, item_pedido, pagamento,
    papel, pedido, produto, produto_categoria, usuario_papel, user
)

DATABASE_URI = 'sqlite:///app.db'
args = {'check_same_thread': False}
engine = create_engine(DATABASE_URI, connect_args=args)


def create_database():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(bind=engine) as session:
        yield session
